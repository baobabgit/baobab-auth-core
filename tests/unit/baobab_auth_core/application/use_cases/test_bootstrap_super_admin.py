"""Tests du cas d'usage BootstrapSuperAdmin.

:spec: BL-050-008
"""

from datetime import UTC, datetime

import pytest

from baobab_auth_core.application.commands.bootstrap_super_admin_command import (
    BootstrapSuperAdminCommand,
)
from baobab_auth_core.application.use_cases.bootstrap_super_admin import (
    BootstrapSuperAdmin,
)
from baobab_auth_core.domain.entities.user import User
from baobab_auth_core.domain.enums.audit_event_type import AuditEventType
from baobab_auth_core.domain.enums.user_status import UserStatus
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.email import Email
from baobab_auth_core.domain.value_objects.password_hash import PasswordHash
from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.domain.value_objects.user_id import UserId
from baobab_auth_core.exceptions.authorization import ForbiddenError

_NOW = datetime(2024, 1, 1, tzinfo=UTC)


def _user(uid: str) -> User:
    return User(
        id=UserId(uid),
        auth_subject=AuthSubject(f"subj-{uid}"),
        email=Email(f"{uid}@example.com"),
        password_hash=PasswordHash("hash-1"),
        status=UserStatus.ACTIVE,
        role_names=(),
        created_at=_NOW,
        updated_at=_NOW,
    )


class TestBootstrapSuperAdmin:
    def test_BL_050_008_1_amorce_premier_super_admin(  # type: ignore[no-untyped-def]
        self, users, roles, audit, ids, clock, uow
    ) -> None:
        users.save(_user("first"))
        BootstrapSuperAdmin(users, roles, audit, ids, clock, uow).execute(
            BootstrapSuperAdminCommand(target_user_id="first")
        )
        assert users.get_by_id(UserId("first")).has_role(RoleName("SUPER_ADMIN"))
        assert any(
            e.event_type == AuditEventType.ROLE_ASSIGNED for e in audit.all_events
        )

    def test_BL_050_008_2_refuse_si_super_admin_existe(  # type: ignore[no-untyped-def]
        self, users, roles, audit, ids, clock, uow
    ) -> None:
        roles.set_users_with_role_count(RoleName("SUPER_ADMIN"), 1)
        users.save(_user("second"))
        with pytest.raises(ForbiddenError):
            BootstrapSuperAdmin(users, roles, audit, ids, clock, uow).execute(
                BootstrapSuperAdminCommand(target_user_id="second")
            )
