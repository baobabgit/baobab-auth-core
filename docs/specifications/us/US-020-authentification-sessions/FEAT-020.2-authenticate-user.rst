FEAT-020.2 — Implémenter AuthenticateUser
=========================================

:Rattachée à: :ref:`us-020`
:Backlog: ``BL-020-002``
:Statut: Implémentée

Description
-----------

Cas d'usage `AuthenticateUser` + commande/résultat, émission de session et tokens.

Critères d'acceptation
----------------------

#. Message d'échec générique, ne divulgue pas l'existence de l'email.
#. Vérifie le mot de passe via `PasswordHasher`, refuse `DISABLED`/`DELETED`/`LOCKED`.
#. Crée une session active + `refresh_token_id`, émet une `TokenPair` via `TokenProvider`.
#. Produit `LOGIN_SUCCESS` / `LOGIN_FAILURE`, commit atomique.
