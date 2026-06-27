"""Port Clock — fournisseur de l'heure courante.

:spec: BL-010-006
"""

from datetime import datetime
from typing import Protocol, runtime_checkable


@runtime_checkable
class Clock(Protocol):
    """Protocole d'abstraction de l'horloge système.

    Permet d'injecter une horloge déterministe dans les tests.
    """

    def now(self) -> datetime:
        """Retourne l'heure courante en UTC.

        :returns: Datetime UTC-aware.
        """
        ...
