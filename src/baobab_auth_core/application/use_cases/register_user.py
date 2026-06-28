"""Cas d'usage RegisterUser — inscription d'un nouvel utilisateur.

:spec: BL-020-001
"""

from baobab_auth_core.application.commands.register_user_command import (
    RegisterUserCommand,
)
from baobab_auth_core.application.results.authenticated_user import AuthenticatedUser
from baobab_auth_core.application.results.register_user_result import RegisterUserResult
from baobab_auth_core.application.services.audit_recorder import AuditRecorder
from baobab_auth_core.domain.entities.user import User
from baobab_auth_core.domain.enums.audit_event_type import AuditEventType
from baobab_auth_core.domain.enums.audit_severity import AuditSeverity
from baobab_auth_core.domain.enums.user_status import UserStatus
from baobab_auth_core.domain.policies.password_policy import PasswordPolicy
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.email import Email
from baobab_auth_core.domain.value_objects.plain_password import PlainPassword
from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.domain.value_objects.user_id import UserId
from baobab_auth_core.exceptions.user import UserAlreadyExistsError
from baobab_auth_core.ports.audit_repository import AuditRepository
from baobab_auth_core.ports.clock import Clock
from baobab_auth_core.ports.id_generator import IdGenerator
from baobab_auth_core.ports.password_hasher import PasswordHasher
from baobab_auth_core.ports.unit_of_work import UnitOfWork
from baobab_auth_core.ports.user_repository import UserRepository

_DEFAULT_ROLE = RoleName("USER")


class RegisterUser:
    """Inscrit un nouvel utilisateur et produit l'audit ``USER_REGISTERED``.

    Orchestration : normalisation/validation, hachage, création de l'utilisateur,
    attribution du rôle par défaut, audit, commit atomique.
    """

    def __init__(
        self,
        users: UserRepository,
        audit: AuditRepository,
        password_hasher: PasswordHasher,
        id_generator: IdGenerator,
        clock: Clock,
        uow: UnitOfWork,
        password_policy: PasswordPolicy | None = None,
        default_role: RoleName | None = _DEFAULT_ROLE,
    ) -> None:
        """Initialise le cas d'usage avec ses dépendances injectées.

        :param users: Dépôt d'utilisateurs.
        :param audit: Dépôt d'audit.
        :param password_hasher: Port de hachage de mot de passe.
        :param id_generator: Générateur d'identifiants.
        :param clock: Horloge injectée.
        :param uow: Unité de travail transactionnelle.
        :param password_policy: Politique de mot de passe (défaut : OWASP minimal).
        :param default_role: Rôle attribué à l'inscription (ou None).
        """
        self._users = users
        self._hasher = password_hasher
        self._ids = id_generator
        self._clock = clock
        self._uow = uow
        self._policy = password_policy or PasswordPolicy()
        self._default_role = default_role
        self._recorder = AuditRecorder(audit, id_generator, clock)

    def execute(self, command: RegisterUserCommand) -> RegisterUserResult:
        """Exécute l'inscription.

        :param command: Données d'inscription.
        :returns: Résultat contenant l'utilisateur inscrit (sans secret).
        :raises InvalidEmailError: Si l'email est invalide.
        :raises WeakPasswordError: Si le mot de passe est trop faible.
        :raises UserAlreadyExistsError: Si l'email est déjà utilisé.
        """
        email = Email(command.email)
        password = PlainPassword(command.password)
        self._policy.validate(password, email)

        if self._users.exists_by_email(email):
            raise UserAlreadyExistsError("Un compte existe déjà pour cet email.")

        password_hash = self._hasher.hash(password)
        now = self._clock.now()
        role_names: tuple[RoleName, ...] = (
            (self._default_role,) if self._default_role is not None else ()
        )
        user = User(
            id=UserId(self._ids.generate()),
            auth_subject=AuthSubject(self._ids.generate()),
            email=email,
            password_hash=password_hash,
            status=UserStatus.ACTIVE,
            role_names=role_names,
            created_at=now,
            updated_at=now,
        )

        with self._uow:
            self._users.save(user)
            self._recorder.record(
                event_type=AuditEventType.USER_REGISTERED,
                severity=AuditSeverity.INFO,
                actor_subject=user.auth_subject,
                target_type="user",
                target_id=str(user.id),
                ip_address=command.ip_address,
                user_agent=command.user_agent,
            )
            self._uow.commit()

        return RegisterUserResult(user=AuthenticatedUser.from_user(user))
