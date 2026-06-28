"""Cas d'usage AuthenticateUser — authentification et création de session.

:spec: BL-020-002, BL-020-003
"""

from datetime import datetime, timedelta

from baobab_auth_core.application.commands.authenticate_user_command import (
    AuthenticateUserCommand,
)
from baobab_auth_core.application.results.authenticate_user_result import (
    AuthenticateUserResult,
)
from baobab_auth_core.application.results.authenticated_user import AuthenticatedUser
from baobab_auth_core.application.results.session_dto import SessionDTO
from baobab_auth_core.application.services.audit_recorder import AuditRecorder
from baobab_auth_core.application.services.token_issuer import TokenIssuer
from baobab_auth_core.domain.entities.session import Session
from baobab_auth_core.domain.entities.user import User
from baobab_auth_core.domain.enums.audit_event_type import AuditEventType
from baobab_auth_core.domain.enums.audit_severity import AuditSeverity
from baobab_auth_core.domain.enums.session_status import SessionStatus
from baobab_auth_core.domain.enums.user_status import UserStatus
from baobab_auth_core.domain.policies.session_policy import SessionPolicy
from baobab_auth_core.domain.value_objects.email import Email
from baobab_auth_core.domain.value_objects.plain_password import PlainPassword
from baobab_auth_core.domain.value_objects.session_id import SessionId
from baobab_auth_core.exceptions.auth import InvalidCredentialsError
from baobab_auth_core.exceptions.user import (
    UserDeletedError,
    UserDisabledError,
    UserLockedError,
)
from baobab_auth_core.ports.audit_repository import AuditRepository
from baobab_auth_core.ports.clock import Clock
from baobab_auth_core.ports.id_generator import IdGenerator
from baobab_auth_core.ports.password_hasher import PasswordHasher
from baobab_auth_core.ports.session_repository import SessionRepository
from baobab_auth_core.ports.token_provider import TokenProvider
from baobab_auth_core.ports.unit_of_work import UnitOfWork
from baobab_auth_core.ports.user_repository import UserRepository

_GENERIC_FAILURE = "Identifiants invalides."
_FAILURE_METADATA = {"reason": "invalid_credentials"}


class AuthenticateUser:
    """Authentifie un utilisateur, gère le lockout et ouvre une session.

    Le message d'échec est générique : l'existence de l'email n'est jamais
    divulguée lors de la vérification des identifiants.
    """

    def __init__(
        self,
        users: UserRepository,
        sessions: SessionRepository,
        audit: AuditRepository,
        password_hasher: PasswordHasher,
        token_provider: TokenProvider,
        id_generator: IdGenerator,
        clock: Clock,
        uow: UnitOfWork,
        session_policy: SessionPolicy | None = None,
    ) -> None:
        """Initialise le cas d'usage avec ses dépendances injectées.

        :param users: Dépôt d'utilisateurs.
        :param sessions: Dépôt de sessions.
        :param audit: Dépôt d'audit.
        :param password_hasher: Port de vérification de mot de passe.
        :param token_provider: Port d'émission de tokens.
        :param id_generator: Générateur d'identifiants.
        :param clock: Horloge injectée.
        :param uow: Unité de travail transactionnelle.
        :param session_policy: Politique de session (TTL, lockout).
        """
        self._users = users
        self._sessions = sessions
        self._hasher = password_hasher
        self._tokens = token_provider
        self._ids = id_generator
        self._clock = clock
        self._uow = uow
        self._policy = session_policy or SessionPolicy()
        self._recorder = AuditRecorder(audit, id_generator, clock)
        self._issuer = TokenIssuer(token_provider, self._policy)

    def execute(self, command: AuthenticateUserCommand) -> AuthenticateUserResult:
        """Exécute l'authentification.

        :param command: Données d'authentification.
        :returns: Résultat contenant l'utilisateur, la session et les tokens.
        :raises InvalidCredentialsError: Email inconnu ou mot de passe incorrect.
        :raises UserLockedError: Compte verrouillé.
        :raises UserDisabledError: Compte désactivé.
        :raises UserDeletedError: Compte supprimé.
        """
        email = Email(command.email)
        password = PlainPassword(command.password)
        now = self._clock.now()

        user = self._users.get_by_email(email)
        if user is None:
            self._commit_failure(None, command)
            raise InvalidCredentialsError(_GENERIC_FAILURE)

        self._ensure_account_usable(user, command, now)

        if not self._hasher.verify(password, user.password_hash):
            self._handle_bad_password(user, command, now)
            raise InvalidCredentialsError(_GENERIC_FAILURE)

        return self._succeed(user, command, now)

    def _ensure_account_usable(
        self,
        user: User,
        command: AuthenticateUserCommand,
        now: datetime,
    ) -> None:
        """Vérifie l'état du compte, avec auto-déverrouillage si le délai est passé.

        :param user: Utilisateur concerné.
        :param command: Commande d'authentification.
        :param now: Horodatage courant (UTC).
        :raises UserLockedError: Compte encore verrouillé.
        :raises UserDisabledError: Compte désactivé.
        :raises UserDeletedError: Compte supprimé.
        """
        if user.status == UserStatus.LOCKED:
            if user.locked_until is not None and now >= user.locked_until:
                user.unlock(now)
            else:
                self._commit_failure(user, command)
                raise UserLockedError("Le compte est temporairement verrouillé.")
        if user.status == UserStatus.DISABLED:
            self._commit_failure(user, command)
            raise UserDisabledError("Le compte est désactivé.")
        if user.status == UserStatus.DELETED:
            self._commit_failure(user, command)
            raise UserDeletedError("Le compte est supprimé.")

    def _handle_bad_password(
        self,
        user: User,
        command: AuthenticateUserCommand,
        now: datetime,
    ) -> None:
        """Incrémente les échecs, verrouille au seuil et audite l'échec.

        :param user: Utilisateur concerné.
        :param command: Commande d'authentification.
        :param now: Horodatage courant (UTC).
        """
        user.mark_login_failure(now)
        should_lock = user.failed_login_count >= self._policy.max_failed_login_attempts
        if should_lock:
            until = now + timedelta(seconds=self._policy.lockout_duration_seconds)
            user.lock(until, now)
        self._commit_failure(user, command, locked=should_lock)

    def _succeed(
        self,
        user: User,
        command: AuthenticateUserCommand,
        now: datetime,
    ) -> AuthenticateUserResult:
        """Crée la session, émet les tokens et audite le succès.

        :param user: Utilisateur authentifié.
        :param command: Commande d'authentification.
        :param now: Horodatage courant (UTC).
        :returns: Résultat de l'authentification.
        """
        user.mark_login_success(now)
        expires_at = now + timedelta(seconds=self._policy.refresh_token_ttl_seconds)
        session = Session(
            id=SessionId(self._ids.generate()),
            user_id=user.id,
            refresh_token_id=self._tokens.generate_token_id(),
            status=SessionStatus.ACTIVE,
            created_at=now,
            expires_at=expires_at,
            last_used_at=now,
            ip_address=command.ip_address,
            user_agent=command.user_agent,
            device_label=command.device_label,
        )
        tokens = self._issuer.issue(
            subject=user.auth_subject,
            session=session,
            roles=user.role_names,
        )

        with self._uow:
            self._users.save(user)
            self._sessions.save(session)
            self._recorder.record(
                event_type=AuditEventType.LOGIN_SUCCESS,
                severity=AuditSeverity.INFO,
                actor_subject=user.auth_subject,
                target_type="user",
                target_id=str(user.id),
                ip_address=command.ip_address,
                user_agent=command.user_agent,
            )
            self._uow.commit()

        return AuthenticateUserResult(
            user=AuthenticatedUser.from_user(user),
            session=SessionDTO.from_session(session),
            tokens=tokens,
        )

    def _commit_failure(
        self,
        user: User | None,
        command: AuthenticateUserCommand,
        locked: bool = False,
    ) -> None:
        """Persiste l'audit d'échec (et l'utilisateur si modifié) atomiquement.

        :param user: Utilisateur concerné (ou None si inconnu).
        :param command: Commande d'authentification.
        :param locked: ``True`` si un événement ``ACCOUNT_LOCKED`` doit être émis.
        """
        actor = user.auth_subject if user is not None else None
        target_id = str(user.id) if user is not None else None
        target_type = "user" if user is not None else None
        with self._uow:
            if user is not None:
                self._users.save(user)
            if locked and user is not None:
                self._recorder.record(
                    event_type=AuditEventType.ACCOUNT_LOCKED,
                    severity=AuditSeverity.WARNING,
                    actor_subject=actor,
                    target_type="user",
                    target_id=target_id,
                    ip_address=command.ip_address,
                    user_agent=command.user_agent,
                )
            self._recorder.record(
                event_type=AuditEventType.LOGIN_FAILURE,
                severity=AuditSeverity.WARNING,
                actor_subject=actor,
                target_type=target_type,
                target_id=target_id,
                ip_address=command.ip_address,
                user_agent=command.user_agent,
                metadata=dict(_FAILURE_METADATA),
            )
            self._uow.commit()
