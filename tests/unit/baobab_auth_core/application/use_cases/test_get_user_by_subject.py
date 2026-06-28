"""Tests du cas d'usage GetUserBySubject.

:spec: BL-050-007
"""

import pytest

from baobab_auth_core.application.queries.get_user_by_subject_query import (
    GetUserBySubjectQuery,
)
from baobab_auth_core.application.use_cases.get_user_by_subject import GetUserBySubject
from baobab_auth_core.exceptions.user import UserNotFoundError


class TestGetUserBySubject:
    def test_BL_050_007_1_lecture_nominale(  # type: ignore[no-untyped-def]
        self, users, make_active_user
    ) -> None:
        user = make_active_user()
        users.save(user)
        result = GetUserBySubject(users).execute(
            GetUserBySubjectQuery(auth_subject=str(user.auth_subject))
        )
        assert result.email == user.email
        assert not hasattr(result, "password_hash")

    def test_BL_050_007_2_introuvable(self, users) -> None:  # type: ignore[no-untyped-def]
        with pytest.raises(UserNotFoundError):
            GetUserBySubject(users).execute(GetUserBySubjectQuery(auth_subject="ghost"))
