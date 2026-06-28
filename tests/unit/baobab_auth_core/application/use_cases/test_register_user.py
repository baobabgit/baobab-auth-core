"""Tests du cas d'usage RegisterUser.

:spec: BL-020-001
"""

import pytest

from baobab_auth_core.application.commands.register_user_command import (
    RegisterUserCommand,
)
from baobab_auth_core.application.use_cases.register_user import RegisterUser
from baobab_auth_core.domain.enums.audit_event_type import AuditEventType
from baobab_auth_core.domain.enums.user_status import UserStatus
from baobab_auth_core.domain.value_objects.email import Email
from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.exceptions.user import UserAlreadyExistsError
from baobab_auth_core.exceptions.validation import InvalidEmailError, WeakPasswordError

_DEFAULT_ROLE = RoleName("USER")


class TestRegisterUser:
    def _uc(self, users, audit, hasher, ids, clock, uow, default_role=_DEFAULT_ROLE):  # type: ignore[no-untyped-def]
        return RegisterUser(
            users, audit, hasher, ids, clock, uow, default_role=default_role
        )

    def test_BL_020_001_1_inscription_nominale(  # type: ignore[no-untyped-def]
        self, users, audit, hasher, ids, clock, uow, valid_email, valid_password
    ) -> None:
        uc = self._uc(users, audit, hasher, ids, clock, uow)
        result = uc.execute(
            RegisterUserCommand(email=valid_email, password=valid_password)
        )
        assert result.user.email == Email(valid_email)
        assert result.user.status == UserStatus.ACTIVE
        assert RoleName("USER") in result.user.role_names
        assert users.get_by_email(Email(valid_email)) is not None
        assert uow.committed is True
        assert not hasattr(result.user, "password_hash")
        assert any(
            e.event_type == AuditEventType.USER_REGISTERED for e in audit.all_events
        )

    def test_BL_020_001_2_email_deja_utilise(  # type: ignore[no-untyped-def]
        self,
        users,
        audit,
        hasher,
        ids,
        clock,
        uow,
        make_active_user,
        valid_email,
        valid_password,
    ) -> None:
        users.save(make_active_user())
        uc = self._uc(users, audit, hasher, ids, clock, uow)
        with pytest.raises(UserAlreadyExistsError):
            uc.execute(RegisterUserCommand(email=valid_email, password=valid_password))

    def test_BL_020_001_3_mot_de_passe_faible(  # type: ignore[no-untyped-def]
        self, users, audit, hasher, ids, clock, uow, valid_email
    ) -> None:
        uc = self._uc(users, audit, hasher, ids, clock, uow)
        with pytest.raises(WeakPasswordError):
            uc.execute(RegisterUserCommand(email=valid_email, password="short"))

    def test_BL_020_001_4_email_invalide(  # type: ignore[no-untyped-def]
        self, users, audit, hasher, ids, clock, uow, valid_password
    ) -> None:
        uc = self._uc(users, audit, hasher, ids, clock, uow)
        with pytest.raises(InvalidEmailError):
            uc.execute(
                RegisterUserCommand(email="not-an-email", password=valid_password)
            )

    def test_BL_020_001_5_sans_role_par_defaut(  # type: ignore[no-untyped-def]
        self, users, audit, hasher, ids, clock, uow, valid_email, valid_password
    ) -> None:
        uc = self._uc(users, audit, hasher, ids, clock, uow, default_role=None)
        result = uc.execute(
            RegisterUserCommand(email=valid_email, password=valid_password)
        )
        assert result.user.role_names == ()
