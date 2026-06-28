"""Tests du cas d'usage ListUserSessions.

:spec: BL-050-007
"""

from datetime import UTC, datetime

import pytest

from baobab_auth_core.application.queries.list_user_sessions_query import (
    ListUserSessionsQuery,
)
from baobab_auth_core.application.use_cases.list_user_sessions import ListUserSessions
from baobab_auth_core.domain.entities.session import Session
from baobab_auth_core.domain.entities.user import User
from baobab_auth_core.domain.enums.session_status import SessionStatus
from baobab_auth_core.domain.enums.user_status import UserStatus
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.email import Email
from baobab_auth_core.domain.value_objects.password_hash import PasswordHash
from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.domain.value_objects.session_id import SessionId
from baobab_auth_core.domain.value_objects.token_id import TokenId
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


def _session(uid: str, sid: str) -> Session:
    return Session(
        id=SessionId(sid),
        user_id=UserId(uid),
        refresh_token_id=TokenId(f"rt-{sid}"),
        status=SessionStatus.ACTIVE,
        created_at=_NOW,
        expires_at=datetime(2099, 1, 1, tzinfo=UTC),
    )


class TestListUserSessions:
    def test_BL_050_007_1_proprietaire_liste_ses_sessions(  # type: ignore[no-untyped-def]
        self, users, sessions, roles, permissions, authorization
    ) -> None:
        users.save(_user("alice", "USER"))
        sessions.save(_session("alice", "s1"))
        result = ListUserSessions(users, sessions, authorization).execute(
            ListUserSessionsQuery(actor_subject="subj-alice", target_user_id="alice")
        )
        assert len(result) == 1
        assert not hasattr(result[0], "refresh_token_id")

    def test_BL_050_007_2_admin_liste_compte_standard(  # type: ignore[no-untyped-def]
        self, users, sessions, roles, permissions, authorization, make_role
    ) -> None:
        roles.save(make_role("ADMIN"))
        users.save(_user("admin", "ADMIN"))
        users.save(_user("bob", "USER"))
        sessions.save(_session("bob", "s1"))
        result = ListUserSessions(users, sessions, authorization).execute(
            ListUserSessionsQuery(actor_subject="subj-admin", target_user_id="bob")
        )
        assert len(result) == 1

    def test_BL_050_007_3_non_autorise_refuse(  # type: ignore[no-untyped-def]
        self, users, sessions, roles, permissions, authorization
    ) -> None:
        users.save(_user("eve", "USER"))
        users.save(_user("bob", "USER"))
        sessions.save(_session("bob", "s1"))
        with pytest.raises(ForbiddenError):
            ListUserSessions(users, sessions, authorization).execute(
                ListUserSessionsQuery(actor_subject="subj-eve", target_user_id="bob")
            )
