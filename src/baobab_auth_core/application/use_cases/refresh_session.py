"""Cas d'usage RefreshSession — rafraîchissement d'une session et rotation tokens.

:spec: BL-020-004
"""

from baobab_auth_core.application.commands.refresh_session_command import (
    RefreshSessionCommand,
)
from baobab_auth_core.application.results.refresh_session_result import (
    RefreshSessionResult,
)
from baobab_auth_core.application.results.session_dto import SessionDTO
from baobab_auth_core.application.services.audit_recorder import AuditRecorder
from baobab_auth_core.application.services.token_issuer import TokenIssuer
from baobab_auth_core.domain.enums.audit_event_type import AuditEventType
from baobab_auth_core.domain.enums.audit_severity import AuditSeverity
from baobab_auth_core.domain.enums.session_status import SessionStatus
from baobab_auth_core.domain.policies.session_policy import SessionPolicy
from baobab_auth_core.domain.value_objects.token_id import TokenId
from baobab_auth_core.exceptions.auth import TokenInvalidError
from baobab_auth_core.exceptions.session import (
    SessionExpiredError,
    SessionNotFoundError,
    SessionRevokedError,
)
from baobab_auth_core.exceptions.user import UserNotFoundError
from baobab_auth_core.ports.audit_repository import AuditRepository
from baobab_auth_core.ports.clock import Clock
from baobab_auth_core.ports.id_generator import IdGenerator
from baobab_auth_core.ports.session_repository import SessionRepository
from baobab_auth_core.ports.token_provider import TokenProvider
from baobab_auth_core.ports.unit_of_work import UnitOfWork
from baobab_auth_core.ports.user_repository import UserRepository


class RefreshSession:
    """Rafraîchit une session valide et émet une nouvelle paire de tokens.

    Le refresh token brut n'est jamais stocké ni audité ; la session est
    retrouvée par son ``refresh_token_id`` puis le token est tourné (rotation).
    """

    def __init__(
        self,
        sessions: SessionRepository,
        users: UserRepository,
        audit: AuditRepository,
        token_provider: TokenProvider,
        id_generator: IdGenerator,
        clock: Clock,
        uow: UnitOfWork,
        session_policy: SessionPolicy | None = None,
    ) -> None:
        """Initialise le cas d'usage avec ses dépendances injectées.

        :param sessions: Dépôt de sessions.
        :param users: Dépôt d'utilisateurs.
        :param audit: Dépôt d'audit.
        :param token_provider: Port de tokens.
        :param id_generator: Générateur d'identifiants (audit).
        :param clock: Horloge injectée.
        :param uow: Unité de travail transactionnelle.
        :param session_policy: Politique de session.
        """
        self._sessions = sessions
        self._users = users
        self._tokens = token_provider
        self._clock = clock
        self._uow = uow
        self._policy = session_policy or SessionPolicy()
        self._recorder = AuditRecorder(audit, id_generator, clock)
        self._issuer = TokenIssuer(token_provider, self._policy)

    def execute(self, command: RefreshSessionCommand) -> RefreshSessionResult:
        """Exécute le rafraîchissement.

        :param command: Données de rafraîchissement (refresh token brut).
        :returns: Résultat contenant la session et la nouvelle paire de tokens.
        :raises TokenInvalidError: Refresh token invalide ou sans identifiant.
        :raises TokenExpiredError: Refresh token expiré.
        :raises SessionNotFoundError: Aucune session pour ce refresh token.
        :raises SessionRevokedError: Session révoquée.
        :raises SessionExpiredError: Session expirée.
        :raises UserNotFoundError: Utilisateur de la session introuvable.
        """
        payload = self._tokens.verify_refresh_token(command.refresh_token)
        raw_token_id = payload.get("refresh_token_id") or payload.get("jti")
        if not raw_token_id:
            raise TokenInvalidError("Refresh token sans identifiant exploitable.")

        session = self._sessions.get_by_refresh_token_id(TokenId(str(raw_token_id)))
        if session is None:
            raise SessionNotFoundError("Session introuvable pour ce refresh token.")

        now = self._clock.now()
        if session.status == SessionStatus.REVOKED or session.revoked_at is not None:
            raise SessionRevokedError("La session a été révoquée.")
        if session.is_expired(now):
            raise SessionExpiredError("La session a expiré.")

        user = self._users.get_by_id(session.user_id)
        if user is None:
            raise UserNotFoundError("Utilisateur de la session introuvable.")

        session.rotate_refresh_token(self._tokens.generate_token_id(), now)
        tokens = self._issuer.issue(
            subject=user.auth_subject,
            session=session,
            roles=user.role_names,
        )

        with self._uow:
            self._sessions.save(session)
            self._recorder.record(
                event_type=AuditEventType.SESSION_REFRESHED,
                severity=AuditSeverity.INFO,
                actor_subject=user.auth_subject,
                target_type="session",
                target_id=str(session.id),
                ip_address=command.ip_address,
                user_agent=command.user_agent,
            )
            self._uow.commit()

        return RefreshSessionResult(
            session=SessionDTO.from_session(session),
            tokens=tokens,
        )
