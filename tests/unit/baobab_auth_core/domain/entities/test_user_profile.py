"""Tests de l'entité UserProfile."""

from datetime import UTC, datetime

from baobab_auth_core.domain.entities.user_profile import UserProfile
from baobab_auth_core.domain.value_objects.user_id import UserId

_NOW = datetime(2024, 1, 1, tzinfo=UTC)


class TestUserProfile:
    def test_BL_010_003_1_construction_minimal(self) -> None:
        p = UserProfile(
            user_id=UserId("u1"),
            created_at=_NOW,
            updated_at=_NOW,
        )
        assert p.user_id == UserId("u1")
        assert p.display_name is None
        assert p.locale is None
        assert p.timezone is None
        assert p.avatar_url is None

    def test_BL_010_003_2_construction_full(self) -> None:
        p = UserProfile(
            user_id=UserId("u1"),
            created_at=_NOW,
            updated_at=_NOW,
            display_name="Alice",
            locale="fr-FR",
            timezone="Europe/Paris",
            avatar_url="https://example.com/avatar.png",
        )
        assert p.display_name == "Alice"
        assert p.locale == "fr-FR"
        assert p.timezone == "Europe/Paris"

    def test_BL_010_003_3_no_secrets(self) -> None:
        p = UserProfile(
            user_id=UserId("u1"),
            created_at=_NOW,
            updated_at=_NOW,
        )
        assert not hasattr(p, "password_hash")
        assert not hasattr(p, "password")
