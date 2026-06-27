"""Tests du FakeClock."""

from datetime import UTC, datetime

from baobab_auth_core.testing.fake_clock import FakeClock


class TestFakeClock:
    def test_BL_010_007_1_default_time(self) -> None:
        clock = FakeClock()
        assert clock.now().tzinfo is not None

    def test_BL_010_007_2_fixed_time(self) -> None:
        fixed = datetime(2025, 6, 15, 12, 0, 0, tzinfo=UTC)
        clock = FakeClock(fixed_time=fixed)
        assert clock.now() == fixed

    def test_BL_010_007_3_set_now(self) -> None:
        clock = FakeClock()
        new_time = datetime(2030, 1, 1, tzinfo=UTC)
        clock.set_now(new_time)
        assert clock.now() == new_time

    def test_BL_010_007_4_advance(self) -> None:
        start = datetime(2024, 1, 1, 0, 0, 0, tzinfo=UTC)
        clock = FakeClock(fixed_time=start)
        clock.advance(3600)
        assert clock.now().hour == 1

    def test_BL_010_007_5_advance_negative(self) -> None:
        start = datetime(2024, 1, 1, 1, 0, 0, tzinfo=UTC)
        clock = FakeClock(fixed_time=start)
        clock.advance(-3600)
        assert clock.now().hour == 0
