"""Tests de l'exception de base BaobabAuthCoreError."""

import pytest

from baobab_auth_core.exceptions.base import BaobabAuthCoreError


class TestBaobabAuthCoreError:
    def test_BL_010_005_1_is_exception(self) -> None:
        err = BaobabAuthCoreError("test")
        assert isinstance(err, Exception)

    def test_BL_010_005_2_message_stored(self) -> None:
        err = BaobabAuthCoreError("oops")
        assert err.message == "oops"
        assert str(err) == "oops"

    def test_BL_010_005_3_default_empty_message(self) -> None:
        err = BaobabAuthCoreError()
        assert err.message == ""

    def test_BL_010_005_4_can_raise(self) -> None:
        with pytest.raises(BaobabAuthCoreError, match="boom"):
            raise BaobabAuthCoreError("boom")
