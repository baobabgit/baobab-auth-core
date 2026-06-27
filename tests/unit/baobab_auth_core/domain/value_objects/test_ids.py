"""Tests des value objects d'identifiants (UserId, RoleId, PermissionId, etc.)."""

import dataclasses

import pytest

from baobab_auth_core.domain.value_objects.audit_event_id import AuditEventId
from baobab_auth_core.domain.value_objects.permission_id import PermissionId
from baobab_auth_core.domain.value_objects.role_id import RoleId
from baobab_auth_core.domain.value_objects.session_id import SessionId
from baobab_auth_core.domain.value_objects.token_id import TokenId
from baobab_auth_core.domain.value_objects.user_id import UserId
from baobab_auth_core.exceptions.validation import ValidationError

_ID_CLASSES = [UserId, RoleId, PermissionId, SessionId, TokenId, AuditEventId]


class TestUserId:
    def test_BL_010_002_1_valid(self) -> None:
        uid = UserId("abc-123")
        assert uid.value == "abc-123"

    def test_BL_010_002_2_raises_on_empty(self) -> None:
        with pytest.raises(ValidationError):
            UserId("")

    def test_BL_010_002_3_raises_on_whitespace(self) -> None:
        with pytest.raises(ValidationError):
            UserId("   ")

    def test_BL_010_002_4_str(self) -> None:
        assert str(UserId("x")) == "x"

    def test_BL_010_002_5_repr(self) -> None:
        assert "x" in repr(UserId("x"))

    def test_BL_010_002_6_equality(self) -> None:
        assert UserId("a") == UserId("a")
        assert UserId("a") != UserId("b")

    def test_BL_010_002_7_frozen(self) -> None:
        uid = UserId("abc")
        with pytest.raises(dataclasses.FrozenInstanceError):
            uid.value = "xyz"  # type: ignore[misc]


class TestRoleId:
    def test_BL_010_002_8_valid(self) -> None:
        assert RoleId("r1").value == "r1"

    def test_BL_010_002_9_raises_empty(self) -> None:
        with pytest.raises(ValidationError):
            RoleId("")

    def test_BL_010_002_10_str_repr(self) -> None:
        r = RoleId("r1")
        assert str(r) == "r1"
        assert "r1" in repr(r)


class TestPermissionId:
    def test_BL_010_002_11_valid(self) -> None:
        assert PermissionId("p1").value == "p1"

    def test_BL_010_002_12_raises_empty(self) -> None:
        with pytest.raises(ValidationError):
            PermissionId("")

    def test_BL_010_002_13_str_repr(self) -> None:
        p = PermissionId("p1")
        assert str(p) == "p1"
        assert "p1" in repr(p)


class TestSessionId:
    def test_BL_010_002_14_valid(self) -> None:
        assert SessionId("s1").value == "s1"

    def test_BL_010_002_15_raises_empty(self) -> None:
        with pytest.raises(ValidationError):
            SessionId("")

    def test_BL_010_002_16_str_repr(self) -> None:
        s = SessionId("s1")
        assert str(s) == "s1"
        assert "s1" in repr(s)


class TestTokenId:
    def test_BL_010_002_17_valid(self) -> None:
        assert TokenId("t1").value == "t1"

    def test_BL_010_002_18_raises_empty(self) -> None:
        with pytest.raises(ValidationError):
            TokenId("")

    def test_BL_010_002_19_str_repr(self) -> None:
        t = TokenId("t1")
        assert str(t) == "t1"
        assert "t1" in repr(t)


class TestAuditEventId:
    def test_BL_010_002_20_valid(self) -> None:
        assert AuditEventId("e1").value == "e1"

    def test_BL_010_002_21_raises_empty(self) -> None:
        with pytest.raises(ValidationError):
            AuditEventId("")

    def test_BL_010_002_22_str_repr(self) -> None:
        a = AuditEventId("e1")
        assert str(a) == "e1"
        assert "e1" in repr(a)

    def test_BL_010_002_23_equality(self) -> None:
        assert AuditEventId("e1") == AuditEventId("e1")
