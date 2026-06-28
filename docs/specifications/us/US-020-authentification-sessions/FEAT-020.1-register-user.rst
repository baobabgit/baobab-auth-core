FEAT-020.1 — Implémenter RegisterUser
=====================================

:Rattachée à: :ref:`us-020`
:Backlog: ``BL-020-001``
:Statut: Implémentée

Description
-----------

Cas d'usage `RegisterUser` + `RegisterUserCommand`/`RegisterUserResult`.

Critères d'acceptation
----------------------

#. Normalise l'email et refuse un email déjà existant (`UserAlreadyExistsError`).
#. Valide le mot de passe via `PasswordPolicy` (`WeakPasswordError`).
#. Hashe via `PasswordHasher`, génère `UserId`/`AuthSubject` via `IdGenerator`.
#. Attribue le rôle `USER` si disponible, produit l'audit `USER_REGISTERED`, commit atomique.
