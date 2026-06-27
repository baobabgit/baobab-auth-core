"""Port IdGenerator — générateur d'identifiants uniques.

:spec: BL-010-006
"""

from typing import Protocol, runtime_checkable


@runtime_checkable
class IdGenerator(Protocol):
    """Protocole de génération d'identifiants uniques.

    Permet d'injecter un générateur déterministe dans les tests.
    """

    def generate(self) -> str:
        """Génère un identifiant unique sous forme de chaîne.

        :returns: Identifiant unique (ex. UUID v4).
        """
        ...
