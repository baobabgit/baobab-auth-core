FEAT-010.2 — Implémenter les value objects
==========================================

:Rattachée à: :ref:`us-010`
:Issue GitHub: ``[FEAT-010.2]`` (sub-issue de ``[US-010]``)
:Backlog: ``BL-010-002``
:Statut: Implémentée

Description
-----------

Fournir les value objects métier sous forme de **frozen dataclasses** immuables,
comparables par valeur, normalisant et validant leur contenu à la construction.

Value objects livrés
--------------------

``Email``, ``AuthSubject``, ``PlainPassword``, ``PasswordHash``, ``RoleName``,
``PermissionName``, et les identifiants typés ``UserId``, ``RoleId``,
``PermissionId``, ``SessionId``, ``TokenId``, ``AuditEventId``.

Critères d'acceptation
----------------------

#. ``Email`` normalise en minuscules et exige la présence d'un ``@`` ; sinon lève
   ``InvalidEmailError``.
#. ``RoleName`` normalise en majuscules et refuse vide/espaces ; sinon lève
   ``InvalidRoleNameError``.
#. ``PermissionName`` valide le format ``scope:resource:action`` (3 segments non
   vides) ; sinon lève ``InvalidPermissionNameError``.
#. ``PlainPassword`` et ``PasswordHash`` masquent leur valeur dans ``repr()`` et
   ``str()`` (rendu ``"***"``).
#. Tout identifiant typé refuse une valeur vide ou blanche.
#. Toute tentative de mutation lève ``dataclasses.FrozenInstanceError``.

Tâches (suivies dans ``docs/backlog/``)
---------------------------------------

* ``TASK-010.2.1`` Implémenter chaque value object (1 classe = 1 fichier).
* ``TASK-010.2.2`` Couvrir normalisation, validation et masquage par des tests.
