"""Fake IdGenerator — générateur d'identifiants déterministe pour les tests.

:spec: BL-010-007
"""


class FakeIdGenerator:
    """Générateur d'identifiants déterministe pour les tests.

    Génère des identifiants prévisibles de la forme ``id-1``, ``id-2``, etc.

    :param prefix: Préfixe des identifiants générés (défaut : ``id``).
    """

    def __init__(self, prefix: str = "id") -> None:
        """Initialise le générateur avec un préfixe et un compteur à 0.

        :param prefix: Préfixe des identifiants.
        """
        self._prefix = prefix
        self._counter = 0

    def generate(self) -> str:
        """Génère un identifiant unique incrémental.

        :returns: Identifiant de la forme ``<prefix>-<n>``.
        """
        self._counter += 1
        return f"{self._prefix}-{self._counter}"

    def reset(self) -> None:
        """Remet le compteur à zéro.

        Utile pour réinitialiser l'état entre deux tests.
        """
        self._counter = 0
