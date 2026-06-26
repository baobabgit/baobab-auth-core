"""Tests du InMemoryUnitOfWork."""

import pytest

from baobab_auth_core.testing.in_memory_unit_of_work import InMemoryUnitOfWork


class TestInMemoryUnitOfWork:
    def test_BL_010_007_1_commit(self) -> None:
        uow = InMemoryUnitOfWork()
        with uow:
            uow.commit()
        assert uow.committed is True
        assert uow.rolled_back is False

    def test_BL_010_007_2_rollback_on_exception(self) -> None:
        uow = InMemoryUnitOfWork()
        with pytest.raises(ValueError):
            with uow:
                raise ValueError("boom")
        assert uow.rolled_back is True

    def test_BL_010_007_3_manual_rollback(self) -> None:
        uow = InMemoryUnitOfWork()
        with uow:
            uow.rollback()
        assert uow.rolled_back is True

    def test_BL_010_007_4_commit_outside_context_raises(self) -> None:
        uow = InMemoryUnitOfWork()
        with pytest.raises(RuntimeError, match="commit"):
            uow.commit()

    def test_BL_010_007_5_rollback_outside_context_raises(self) -> None:
        uow = InMemoryUnitOfWork()
        with pytest.raises(RuntimeError, match="rollback"):
            uow.rollback()

    def test_BL_010_007_6_enter_returns_self(self) -> None:
        uow = InMemoryUnitOfWork()
        result = uow.__enter__()
        assert result is uow
        uow.__exit__(None, None, None)

    def test_BL_010_007_7_state_reset_on_enter(self) -> None:
        uow = InMemoryUnitOfWork()
        with uow:
            uow.commit()
        with uow:
            assert uow.committed is False
            assert uow.rolled_back is False
            uow.commit()
