"""Tests du value object PermissionName."""

import pytest

from baobab_auth_core.domain.value_objects.permission_name import PermissionName
from baobab_auth_core.exceptions.validation import InvalidPermissionNameError


class TestPermissionName:
    def test_BL_010_002_1_valid(self) -> None:
        p = PermissionName("auth:user:read")
        assert p.value == "auth:user:read"

    def test_BL_010_002_2_raises_on_empty(self) -> None:
        with pytest.raises(InvalidPermissionNameError):
            PermissionName("")

    def test_BL_010_002_3_raises_on_missing_colons(self) -> None:
        with pytest.raises(InvalidPermissionNameError):
            PermissionName("auth:user")

    def test_BL_010_002_4_raises_on_too_many_parts(self) -> None:
        with pytest.raises(InvalidPermissionNameError):
            PermissionName("auth:user:read:extra")

    def test_BL_010_002_5_raises_on_empty_segment(self) -> None:
        with pytest.raises(InvalidPermissionNameError):
            PermissionName("auth::read")

    def test_BL_010_002_6_equality(self) -> None:
        assert PermissionName("auth:user:read") == PermissionName("auth:user:read")
        assert PermissionName("auth:user:read") != PermissionName("auth:user:write")

    def test_BL_010_002_7_str(self) -> None:
        assert str(PermissionName("a:b:c")) == "a:b:c"

    def test_BL_010_002_8_repr(self) -> None:
        assert "a:b:c" in repr(PermissionName("a:b:c"))
