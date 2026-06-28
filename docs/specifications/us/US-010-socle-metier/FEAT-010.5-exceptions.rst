FEAT-010.5 — Implémenter les exceptions
=======================================

:Rattachée à: :ref:`us-010`
:Issue GitHub: ``[FEAT-010.5]`` (sub-issue de ``[US-010]``)
:Backlog: ``BL-010-005``
:Statut: Implémentée

Description
-----------

Fournir la hiérarchie d'exceptions métier, regroupée par catégorie dans le
sous-package ``exceptions/`` (dérogation à la règle 1 classe = 1 fichier autorisée
pour les hiérarchies d'exceptions courtes).

Hiérarchie livrée
-----------------

* Racine : ``BaobabAuthCoreError``.
* Validation : ``ValidationError``, ``InvalidEmailError``, ``WeakPasswordError``,
  ``InvalidRoleNameError``, ``InvalidPermissionNameError``.
* Comptes : ``UserAlreadyExistsError``, ``UserNotFoundError``, ``UserDisabledError``,
  ``UserLockedError``, ``UserDeletedError``.
* Authentification : ``InvalidCredentialsError``, ``TokenInvalidError``,
  ``TokenExpiredError``, ``SessionNotFoundError``, ``SessionExpiredError``,
  ``SessionRevokedError``.
* Autorisation : ``AuthorizationError``, ``ForbiddenError``, ``PermissionDeniedError``,
  ``RoleNotFoundError``, ``PermissionNotFoundError``, ``LastSuperAdminRoleRemovalError``.

Critères d'acceptation
----------------------

#. Toutes les exceptions héritent (directement ou non) de ``BaobabAuthCoreError``.
#. Les exceptions de validation héritent de ``ValidationError`` ; celles
   d'autorisation de ``AuthorizationError``.
#. Aucun message d'exception ne contient de secret (mot de passe, hash, token).

Tâches (suivies dans ``docs/backlog/``)
---------------------------------------

* ``TASK-010.5.1`` Implémenter la hiérarchie par catégorie.
* ``TASK-010.5.2`` Couvrir l'arbre d'héritage et l'absence de secret par des tests.
