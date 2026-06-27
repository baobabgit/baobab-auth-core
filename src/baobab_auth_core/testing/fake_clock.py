"""Fake Clock — horloge déterministe pour les tests.

:spec: BL-010-007
"""

from datetime import UTC, datetime


class FakeClock:
    """Horloge déterministe pour les tests unitaires.

    Permet de contrôler l'heure courante dans les tests.

    :param fixed_time: Heure fixe à retourner (défaut : 2024-01-01T00:00:00Z).
    """

    def __init__(self, fixed_time: datetime | None = None) -> None:
        """Initialise l'horloge avec une heure fixe.

        :param fixed_time: Heure fixe. Si None, utilise 2024-01-01T00:00:00Z.
        """
        self._now: datetime = fixed_time or datetime(2024, 1, 1, 0, 0, 0, tzinfo=UTC)

    def now(self) -> datetime:
        """Retourne l'heure fixe configurée.

        :returns: Datetime UTC-aware fixe.
        """
        return self._now

    def set_now(self, dt: datetime) -> None:
        """Modifie l'heure courante.

        :param dt: Nouvelle heure à utiliser.
        """
        self._now = dt

    def advance(self, seconds: float) -> None:
        """Avance l'horloge du nombre de secondes indiqué.

        :param seconds: Nombre de secondes à ajouter.
        """
        from datetime import timedelta

        self._now = self._now + timedelta(seconds=seconds)
