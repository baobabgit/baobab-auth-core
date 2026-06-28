FEAT-020.7 — Stabiliser les DTO tokens/session
==============================================

:Rattachée à: :ref:`us-020`
:Backlog: ``BL-020-007``
:Statut: Implémentée

Description
-----------

`TokenPair`, `TokenClaims`, `SessionDTO`, `AuthenticatedUser`.

Critères d'acceptation
----------------------

#. `TokenPair` masque les tokens dans `repr()`.
#. `SessionDTO` ne contient aucun refresh token brut.
#. `AuthenticatedUser` n'expose aucun secret (pas de `password_hash`).
