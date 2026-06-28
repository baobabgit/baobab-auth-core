"""Cas d'usage RequestJwkRotation — demande de rotation JWK réservée SUPER_ADMIN.

:spec: BL-040-008
"""

from baobab_auth_core.application.commands.request_jwk_rotation_command import (
    RequestJwkRotationCommand,
)
from baobab_auth_core.application.services.audit_recorder import AuditRecorder
from baobab_auth_core.application.services.authorization_service import (
    AuthorizationService,
)
from baobab_auth_core.domain.enums.audit_event_type import AuditEventType
from baobab_auth_core.domain.enums.audit_severity import AuditSeverity
from baobab_auth_core.domain.policies.role_policy import RolePolicy
from baobab_auth_core.exceptions.authorization import ForbiddenError
from baobab_auth_core.ports.audit_repository import AuditRepository
from baobab_auth_core.ports.clock import Clock
from baobab_auth_core.ports.id_generator import IdGenerator
from baobab_auth_core.ports.unit_of_work import UnitOfWork


class RequestJwkRotation:
    """Enregistre une demande de rotation des clés JWK.

    Action **critique** réservée au rôle ``SUPER_ADMIN`` : un ``ADMIN`` ne peut pas
    la déclencher. Produit l'audit ``JWK_ROTATION_REQUESTED`` (CRITICAL).
    """

    def __init__(
        self,
        authorization: AuthorizationService,
        audit: AuditRepository,
        id_generator: IdGenerator,
        clock: Clock,
        uow: UnitOfWork,
        role_policy: RolePolicy | None = None,
    ) -> None:
        """Initialise le cas d'usage avec ses dépendances injectées.

        :param authorization: Service de construction du contexte acteur.
        :param audit: Dépôt d'audit.
        :param id_generator: Générateur d'identifiants d'audit.
        :param clock: Horloge injectée.
        :param uow: Unité de travail transactionnelle.
        :param role_policy: Politique de rôle (rôle super-admin).
        """
        self._authorization = authorization
        self._clock = clock
        self._uow = uow
        self._policy = role_policy or RolePolicy()
        self._recorder = AuditRecorder(audit, id_generator, clock)

    def execute(self, command: RequestJwkRotationCommand) -> None:
        """Exécute la demande de rotation JWK.

        :param command: Données de la demande.
        :raises ForbiddenError: Si l'acteur n'est pas ``SUPER_ADMIN``.
        """
        actor_context = self._authorization.build_context(command.actor_subject)
        if not actor_context.has_role(self._policy.super_admin_role_name):
            raise ForbiddenError(
                "Seul un SUPER_ADMIN peut demander une rotation des clés JWK."
            )

        metadata = {"reason": command.reason} if command.reason else {}
        with self._uow:
            self._recorder.record(
                event_type=AuditEventType.JWK_ROTATION_REQUESTED,
                severity=AuditSeverity.CRITICAL,
                actor_subject=actor_context.auth_subject,
                target_type="jwk",
                ip_address=command.ip_address,
                user_agent=command.user_agent,
                metadata=metadata,
            )
            self._uow.commit()
