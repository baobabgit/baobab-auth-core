"""Tests de PermissionPolicy.

:spec: BL-030-003
"""

import dataclasses

import pytest

from baobab_auth_core.domain.policies.permission_policy import PermissionPolicy
from baobab_auth_core.domain.value_objects.permission_name import PermissionName
from baobab_auth_core.exceptions.validation import InvalidPermissionNameError


class TestPermissionPolicy:
    def test_BL_030_003_1_validates_permission_name(self) -> None:
        policy = PermissionPolicy()
        policy.validate(PermissionName("auth:user:read"))

    def test_BL_030_003_2_validates_string_permission(self) -> None:
        policy = PermissionPolicy()
        policy.validate(" auth:user:read ")

    def test_BL_030_003_3_rejects_invalid_permission(self) -> None:
        policy = PermissionPolicy()
        with pytest.raises(InvalidPermissionNameError):
            policy.validate("auth:user")

    def test_BL_030_003_4_is_valid_returns_boolean(self) -> None:
        policy = PermissionPolicy()
        assert policy.is_valid("auth:user:read") is True
        assert policy.is_valid("auth:user") is False

    def test_BL_030_003_5_frozen(self) -> None:
        policy = PermissionPolicy()
        with pytest.raises(dataclasses.FrozenInstanceError):
            policy.separator = "/"  # type: ignore[misc]
