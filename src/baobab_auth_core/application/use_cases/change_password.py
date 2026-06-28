"""Cas d'usage ChangePassword — changement de mot de passe durci.

:spec: BL-040-013
"""

from datetime import datetime

from baobab_auth_core.application.commands.change_password_command import (
    ChangePasswordCommand,
)
from baobab_auth_core.application.services.audit_recorder import AuditRecorder
from baobab_auth_core.domain.entities.session import Session
from baobab_auth_core.domain.enums.audit_event_type import AuditEventType
from baobab_auth_core.domain.enums.audit_severity import AuditSeverity
from baobab_auth_core.domain.policies.password_policy import PasswordPolicy
from baobab_auth_core.domain.policies.session_policy import SessionPolicy
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.plain_password import PlainPassword
from baobab_auth_core.domain.value_objects.user_id import UserId
from baobab_auth_core.exceptions.auth import InvalidCredentialsError
from baobab_auth_core.exceptions.user import UserNotFoundError
from baobab_auth_core.exceptions.validation import ValidationError
from baobab_auth_core.ports.audit_repository import AuditRepository
from baobab_auth_core.ports.clock import Clock
from baobab_auth_core.ports.id_generator import IdGenerator
from baobab_auth_core.ports.password_hasher import PasswordHasher
from baobab_auth_core.ports.session_repository import SessionRepository
from baobab_auth_core.ports.unit_of_work import UnitOfWork
from baobab_auth_core.ports.user_repository import UserRepository


class ChangePassword:
    """Change le mot de passe d'un utilisateur après vérification de l'ancien.

    Vérifie l'ancien mot de passe, valide le nouveau (différent et conforme à la
    politique), le hache via le port, révoque les autres sessions selon la policy
    et produit l'audit ``PASSWORD_CHANGED`` sans secret.
    """

    def __init__(
        self,
        users: UserRepository,
        sessions: SessionRepository,
        audit: AuditRepository,
        password_hasher: PasswordHasher,
        id_generator: IdGenerator,
        clock: Clock,
        uow: UnitOfWork,
        password_policy: PasswordPolicy | None = None,
        session_policy: SessionPolicy | None = None,
    ) -> None:
        """Initialise le cas d'usage avec ses dépendances injectées.

        :param users: Dépôt d'utilisateurs.
        :param sessions: Dépôt de sessions.
        :param audit: Dépôt d'audit.
        :param password_hasher: Port de hachage/vérification.
        :param id_generator: Générateur d'identifiants d'audit.
        :param clock: Horloge injectée.
        :param uow: Unité de travail transactionnelle.
        :param password_policy: Politique de mot de passe.
        :param session_policy: Politique de session (révocation des autres sessions).
        """
        self._users = users
        self._sessions = sessions
        self._hasher = password_hasher
        self._clock = clock
        self._uow = uow
        self._password_policy = password_policy or PasswordPolicy()
        self._session_policy = session_policy or SessionPolicy()
        self._recorder = AuditRecorder(audit, id_generator, clock)

    def execute(self, command: ChangePasswordCommand) -> int:
        """Exécute le changement de mot de passe.

        :param command: Données du changement.
        :returns: Nombre de sessions révoquées.
        :raises UserNotFoundError: Si l'utilisateur n'existe pas.
        :raises InvalidCredentialsError: Si l'ancien mot de passe est incorrect.
        :raises WeakPasswordError: Si le nouveau mot de passe est trop faible.
        :raises ValidationError: Si le nouveau mot de passe est identique à l'ancien.
        """
        subject = self._coerce_subject(command.auth_subject)
        user = self._users.get_by_auth_subject(subject)
        if user is None:
            raise UserNotFoundError("Utilisateur introuvable.")

        old_password = PlainPassword(command.old_password)
        if not self._hasher.verify(old_password, user.password_hash):
            raise InvalidCredentialsError("Mot de passe actuel incorrect.")

        new_password = PlainPassword(command.new_password)
        self._password_policy.validate(new_password, user.email)
        if self._hasher.verify(new_password, user.password_hash):
            raise ValidationError(
                "Le nouveau mot de passe doit être différent de l'ancien."
            )

        now = self._clock.now()
        user.change_password_hash(self._hasher.hash(new_password), now)

        revoked = self._revoke_other_sessions(user.id, now)
        with self._uow:
            self._users.save(user)
            for session in revoked:
                self._sessions.save(session)
            self._recorder.record(
                event_type=AuditEventType.PASSWORD_CHANGED,
                severity=AuditSeverity.WARNING,
                actor_subject=user.auth_subject,
                target_type="user",
                target_id=str(user.id),
                ip_address=command.ip_address,
                user_agent=command.user_agent,
                metadata={"sessions_revoked": len(revoked)},
            )
            self._uow.commit()
        return len(revoked)

    def _revoke_other_sessions(self, user_id: UserId, now: datetime) -> list[Session]:
        """Révoque les sessions actives si la policy l'exige.

        :param user_id: Identifiant de l'utilisateur.
        :param now: Horodatage courant (UTC).
        :returns: Sessions révoquées (mutées).
        """
        if not self._session_policy.revoke_other_sessions_on_password_change:
            return []
        revoked: list[Session] = []
        for session in self._sessions.get_active_by_user(user_id):
            session.revoke(now)
            revoked.append(session)
        return revoked

    @staticmethod
    def _coerce_subject(subject: AuthSubject | str) -> AuthSubject:
        """Convertit un sujet texte en :class:`AuthSubject`.

        :param subject: Sujet à convertir.
        :returns: Sujet d'authentification.
        """
        if isinstance(subject, AuthSubject):
            return subject
        return AuthSubject(subject)
