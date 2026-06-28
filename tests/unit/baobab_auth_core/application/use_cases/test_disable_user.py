"""Tests du cas d'usage DisableUser.

:spec: BL-050-008
"""

from datetime import UTC, datetime

import pytest

from baobab_auth_core.application.commands.disable_user_command import (
    DisableUserCommand,
)
from baobab_auth_core.application.use_cases.disable_user import DisableUser
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


def _user(uid: str, role: str) -> User:
    return User(
        id=UserId(uid),
        auth_subject=AuthSubject(f"subj-{uid}"),
        email=Email(f"{uid}@example.com"),
        password_hash=PasswordHash("hash-1"),
        status=UserStatus.ACTIVE,
        role_names=(RoleName(role),),
        created_at=_NOW,
        updated_at=_NOW,
    )


class TestDisableUser:
    def test_BL_050_008_1_admin_desactive_et_audite(  # type: ignore[no-untyped-def]
        self,
        users,
        roles,
        permissions,
        authorization,
        audit,
        ids,
        clock,
        uow,
        make_role,
    ) -> None:
        roles.save(make_role("ADMIN"))
        users.save(_user("admin", "ADMIN"))
        users.save(_user("bob", "USER"))
        DisableUser(users, authorization, audit, ids, clock, uow).execute(
            DisableUserCommand(actor_subject="subj-admin", target_user_id="bob")
        )
        assert users.get_by_id(UserId("bob")).status == UserStatus.DISABLED
        assert any(
            e.event_type == AuditEventType.ACCOUNT_DISABLED for e in audit.all_events
        )

    def test_BL_050_008_2_non_admin_refuse(  # type: ignore[no-untyped-def]
        self, users, roles, permissions, authorization, audit, ids, clock, uow
    ) -> None:
        users.save(_user("eve", "USER"))
        users.save(_user("bob", "USER"))
        with pytest.raises(ForbiddenError):
            DisableUser(users, authorization, audit, ids, clock, uow).execute(
                DisableUserCommand(actor_subject="subj-eve", target_user_id="bob")
            )
