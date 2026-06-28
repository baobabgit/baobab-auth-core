FEAT-020.5 — Implémenter Logout
===============================

:Rattachée à: :ref:`us-020`
:Backlog: ``BL-020-005``
:Statut: Implémentée

Description
-----------

Cas d'usage `Logout` idempotent.

Critères d'acceptation
----------------------

#. L'utilisateur déconnecte sa propre session, opération idempotente.
#. Révoque la session, demande la révocation du token via `TokenProvider` si disponible.
#. Produit `LOGOUT`.
