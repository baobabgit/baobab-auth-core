"""Fake InMemoryUnitOfWork — unité de travail en mémoire pour les tests.

:spec: BL-010-007
"""

from types import TracebackType


class InMemoryUnitOfWork:
    """Unité de travail en mémoire pour les tests unitaires.

    Simule le comportement transactionnel sans persistance réelle.
    Enregistre les appels à :meth:`commit` et :meth:`rollback` pour assertions.
    """

    def __init__(self) -> None:
        """Initialise l'unité de travail avec un état inactif."""
        self.committed = False
        self.rolled_back = False
        self._active = False

    def __enter__(self) -> "InMemoryUnitOfWork":
        """Démarre la transaction.

        :returns: L'unité de travail active.
        """
        self._active = True
        self.committed = False
        self.rolled_back = False
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        """Effectue un rollback automatique en cas d'exception.

        :param exc_type: Type de l'exception.
        :param exc_val: Valeur de l'exception.
        :param exc_tb: Traceback de l'exception.
        :returns: ``None`` pour ne pas supprimer l'exception.
        """
        _ = exc_val
        _ = exc_tb
        if exc_type is not None and not self.committed:
            self.rollback()
        self._active = False
        return None

    def commit(self) -> None:
        """Marque la transaction comme validée.

        :raises RuntimeError: Si appelé en dehors d'un contexte actif.
        """
        if not self._active:
            raise RuntimeError("commit() appelé en dehors d'un contexte actif.")
        self.committed = True

    def rollback(self) -> None:
        """Marque la transaction comme annulée.

        :raises RuntimeError: Si appelé en dehors d'un contexte actif.
        """
        if not self._active:
            raise RuntimeError("rollback() appelé en dehors d'un contexte actif.")
        self.rolled_back = True
