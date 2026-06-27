"""Tests du FakePasswordHasher."""

from baobab_auth_core.domain.value_objects.password_hash import PasswordHash
from baobab_auth_core.domain.value_objects.plain_password import PlainPassword
from baobab_auth_core.testing.fake_password_hasher import FakePasswordHasher


class TestFakePasswordHasher:
    def setup_method(self) -> None:
        self.hasher = FakePasswordHasher()

    def test_BL_010_007_1_hash_prefixes(self) -> None:
        h = self.hasher.hash(PlainPassword("secret"))
        assert h.value.startswith("hashed:")

    def test_BL_010_007_2_verify_correct(self) -> None:
        pw = PlainPassword("secret")
        h = self.hasher.hash(pw)
        assert self.hasher.verify(pw, h) is True

    def test_BL_010_007_3_verify_wrong(self) -> None:
        pw = PlainPassword("secret")
        wrong_hash = PasswordHash("hashed:wrong")
        assert self.hasher.verify(pw, wrong_hash) is False

    def test_BL_010_007_4_deterministic(self) -> None:
        pw = PlainPassword("abc")
        h1 = self.hasher.hash(pw)
        h2 = self.hasher.hash(pw)
        assert h1 == h2
