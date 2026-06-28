"""Tests du service AuthorizationService.

:spec: BL-030-002
"""

from datetime import UTC, datetime

import pytest

from baobab_auth_core.application.services.authorization_service import (
    AuthorizationService,
)
from baobab_auth_core.domain.entities.permission import Permission
from baobab_auth_core.domain.entities.role import Role
from baobab_auth_core.domain.entities.user import User
from baobab_auth_core.domain.enums.user_status import UserStatus
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.email import Email
from baobab_auth_core.domain.value_objects.password_hash import PasswordHash
from baobab_auth_core.domain.value_objects.permission_id import PermissionId
from baobab_auth_core.domain.value_objects.permission_name import PermissionName
from baobab_auth_core.domain.value_objects.role_id import RoleId
from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.domain.value_objects.user_id import UserId
from baobab_auth_core.exceptions.authorization import (
    ForbiddenError,
    PermissionDeniedError,
)
from baobab_auth_core.exceptions.user import UserNotFoundError
from baobab_auth_core.testing.in_memory_permission_repository import (
    InMemoryPermissionRepository,
)
from baobab_auth_core.testing.in_memory_role_repository import InMemoryRoleRepository
from baobab_auth_core.testing.in_memory_user_repository import InMemoryUserRepository

_NOW = datetime(2024, 1, 1, tzinfo=UTC)
_LAST_LOGIN = datetime(2024, 1, 2, tzinfo=UTC)


class TestAuthorizationService:
    def setup_method(self) -> None:
        self.users = InMemoryUserRepository()
        self.roles = InMemoryRoleRepository()
        self.permissions = InMemoryPermissionRepository()
        self.service = AuthorizationService(
            self.users,
            self.roles,
            self.permissions,
        )

    def _make_user(
        self,
        role_names: tuple[RoleName, ...] = (RoleName("USER"),),
    ) -> User:
        return User(
            id=UserId("user-1"),
            auth_subject=AuthSubject("subject-1"),
            email=Email("alice@example.com"),
            password_hash=PasswordHash("hash-1"),
            status=UserStatus.ACTIVE,
            role_names=role_names,
            created_at=_NOW,
            updated_at=_NOW,
            last_login_at=_LAST_LOGIN,
        )

    def _make_role(
        self,
        name: str,
        permission_names: tuple[PermissionName, ...],
    ) -> Role:
        return Role(
            id=RoleId(f"role-{name.lower()}"),
            name=RoleName(name),
            is_system=False,
            created_at=_NOW,
            updated_at=_NOW,
            permission_names=permission_names,
        )

    def _make_permission(self, name: str) -> Permission:
        permission_name = PermissionName(name)
        return Permission(
            id=PermissionId(f"permission-{permission_name.value.replace(':', '-')}"),
            name=permission_name,
            resource=permission_name.value.split(":")[1],
            action=permission_name.value.split(":")[2],
            is_system=False,
            created_at=_NOW,
        )

    def test_BL_030_002_1_build_context_agrege_permissions_multi_roles(self) -> None:
        # Arrange
        user_read = PermissionName("auth:user:read")
        role_write = PermissionName("auth:role:write")
        self.permissions.save(self._make_permission("auth:user:read"))
        self.permissions.save(self._make_permission("auth:role:write"))
        self.users.save(
            self._make_user((RoleName("USER"), RoleName("ADMIN"), RoleName("AUDITOR")))
        )
        self.roles.save(self._make_role("USER", (user_read,)))
        self.roles.save(self._make_role("ADMIN", (user_read, role_write)))
        self.roles.save(self._make_role("AUDITOR", (role_write,)))

        # Act
        context = self.service.build_context("subject-1")

        # Assert
        assert context.auth_subject == AuthSubject("subject-1")
        assert context.user_id == UserId("user-1")
        assert context.session_id is None
        assert context.authenticated_at == _LAST_LOGIN
        assert context.roles == (
            RoleName("USER"),
            RoleName("ADMIN"),
            RoleName("AUDITOR"),
        )
        assert context.permissions == (user_read, role_write)

    def test_BL_030_002_2_build_context_ignore_roles_inconnus(self) -> None:
        # Arrange
        self.permissions.save(self._make_permission("auth:user:read"))
        self.users.save(self._make_user((RoleName("USER"), RoleName("OBSOLETE"))))
        self.roles.save(
            self._make_role(
                "USER",
                (
                    PermissionName("auth:user:read"),
                    PermissionName("auth:user:delete"),
                ),
            )
        )

        # Act
        context = self.service.build_context(AuthSubject("subject-1"))

        # Assert
        assert context.roles == (RoleName("USER"),)
        assert context.permissions == (PermissionName("auth:user:read"),)

    def test_BL_030_002_3_build_context_leve_si_utilisateur_absent(self) -> None:
        # Arrange / Act / Assert
        with pytest.raises(UserNotFoundError, match="subject-1"):
            self.service.build_context("subject-1")

    def test_BL_030_002_4_verifie_roles_et_permissions(self) -> None:
        # Arrange
        self.permissions.save(self._make_permission("auth:user:read"))
        self.users.save(self._make_user((RoleName("USER"),)))
        self.roles.save(self._make_role("USER", (PermissionName("auth:user:read"),)))
        context = self.service.build_context("subject-1")

        # Act / Assert
        assert self.service.has_role(context, "user")
        assert not self.service.has_role(context, "admin")
        assert self.service.has_permission(context, "AUTH:USER:READ")
        assert not self.service.has_permission(context, "auth:user:delete")

    def test_BL_030_002_5_require_role_accepte_ou_refuse(self) -> None:
        # Arrange
        self.users.save(self._make_user((RoleName("USER"),)))
        self.roles.save(self._make_role("USER", ()))
        context = self.service.build_context("subject-1")

        # Act / Assert
        self.service.require_role(context, RoleName("USER"))
        with pytest.raises(ForbiddenError, match="ADMIN"):
            self.service.require_role(context, "ADMIN")

    def test_BL_030_002_6_require_permission_accepte_ou_refuse(self) -> None:
        # Arrange
        self.permissions.save(self._make_permission("auth:user:read"))
        self.users.save(self._make_user((RoleName("USER"),)))
        self.roles.save(self._make_role("USER", (PermissionName("auth:user:read"),)))
        context = self.service.build_context("subject-1")

        # Act / Assert
        self.service.require_permission(context, PermissionName("auth:user:read"))
        with pytest.raises(PermissionDeniedError, match="auth:user:delete"):
            self.service.require_permission(context, "auth:user:delete")
