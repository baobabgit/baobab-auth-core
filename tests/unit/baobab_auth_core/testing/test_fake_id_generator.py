"""Tests du FakeIdGenerator."""

from baobab_auth_core.testing.fake_id_generator import FakeIdGenerator


class TestFakeIdGenerator:
    def test_BL_010_007_1_incremental(self) -> None:
        gen = FakeIdGenerator()
        assert gen.generate() == "id-1"
        assert gen.generate() == "id-2"
        assert gen.generate() == "id-3"

    def test_BL_010_007_2_custom_prefix(self) -> None:
        gen = FakeIdGenerator(prefix="user")
        assert gen.generate() == "user-1"

    def test_BL_010_007_3_reset(self) -> None:
        gen = FakeIdGenerator()
        gen.generate()
        gen.generate()
        gen.reset()
        assert gen.generate() == "id-1"

    def test_BL_010_007_4_unique_per_call(self) -> None:
        gen = FakeIdGenerator()
        ids = [gen.generate() for _ in range(5)]
        assert len(set(ids)) == 5
