"""Fake PasswordHasher — hachage déterministe pour les tests.

:spec: BL-010-007
"""

from baobab_auth_core.domain.value_objects.password_hash import PasswordHash
from baobab_auth_core.domain.value_objects.plain_password import PlainPassword

_FAKE_PREFIX = "hashed:"


class FakePasswordHasher:
    """Hacheur de mots de passe déterministe pour les tests.

    Le hash est simplement le mot de passe préfixé par ``hashed:``,
    ce qui permet de vérifier le comportement sans librairie cryptographique.
    """

    def hash(self, password: PlainPassword) -> PasswordHash:
        """Retourne un hash prévisible préfixé par ``hashed:``.

        :param password: Mot de passe en clair.
        :returns: Hash déterministe.
        """
        return PasswordHash(f"{_FAKE_PREFIX}{password.value}")

    def verify(self, password: PlainPassword, password_hash: PasswordHash) -> bool:
        """Vérifie si le mot de passe correspond au hash fake.

        :param password: Mot de passe en clair à vérifier.
        :param password_hash: Hash de référence.
        :returns: ``True`` si le hash correspond.
        """
        return password_hash.value == f"{_FAKE_PREFIX}{password.value}"
