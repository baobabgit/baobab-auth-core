"""Port UnitOfWork — unité de travail transactionnelle.

:spec: BL-010-006
"""

from types import TracebackType
from typing import Protocol, runtime_checkable


@runtime_checkable
class UnitOfWork(Protocol):
    """Protocole d'unité de travail pour la gestion des transactions.

    Utilisé comme gestionnaire de contexte pour garantir l'atomicité
    des opérations de persistance.

    Exemple d'usage::

        with uow:
            uow.users.save(user)
            uow.commit()
    """

    def __enter__(self) -> "UnitOfWork":
        """Démarre la transaction.

        :returns: L'unité de travail active.
        """
        ...

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        """Termine la transaction, effectuant un rollback en cas d'erreur.

        :param exc_type: Type de l'exception (ou None).
        :param exc_val: Valeur de l'exception (ou None).
        :param exc_tb: Traceback de l'exception (ou None).
        :returns: ``False`` pour ne pas supprimer l'exception.
        """
        ...

    def commit(self) -> None:
        """Valide la transaction courante.

        :raises Exception: En cas d'échec de la validation.
        """
        ...

    def rollback(self) -> None:
        """Annule la transaction courante.

        :raises Exception: En cas d'échec du rollback.
        """
        ...
