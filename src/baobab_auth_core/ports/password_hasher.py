"""Port PasswordHasher — hachage et vérification de mots de passe.

:spec: BL-010-006
"""

from typing import Protocol, runtime_checkable

from baobab_auth_core.domain.value_objects.password_hash import PasswordHash
from baobab_auth_core.domain.value_objects.plain_password import PlainPassword


@runtime_checkable
class PasswordHasher(Protocol):
    """Protocole d'abstraction du hachage de mots de passe.

    Les implémentations concrètes utilisent Argon2, bcrypt, etc.
    Ce port garantit que le domaine n'a aucune dépendance sur la librairie de hachage.
    """

    def hash(self, password: PlainPassword) -> PasswordHash:
        """Hache un mot de passe en clair.

        :param password: Mot de passe en clair.
        :returns: Hash du mot de passe.
        """
        ...

    def verify(self, password: PlainPassword, password_hash: PasswordHash) -> bool:
        """Vérifie qu'un mot de passe correspond à son hash.

        :param password: Mot de passe en clair à vérifier.
        :param password_hash: Hash de référence.
        :returns: ``True`` si le mot de passe correspond au hash.
        """
        ...
