FEAT-010.6 — Définir les ports
==============================

:Rattachée à: :ref:`us-010`
:Issue GitHub: ``[FEAT-010.6]`` (sub-issue de ``[US-010]``)
:Backlog: ``BL-010-006``
:Statut: Implémentée

Description
-----------

Définir les frontières de la couche domaine sous forme de ``typing.Protocol``
décorés ``@runtime_checkable``. Le code métier ne connaît que ces interfaces,
jamais les implémentations concrètes.

Ports livrés
-----------

``UserRepository``, ``RoleRepository``, ``PermissionRepository``,
``SessionRepository``, ``AuditRepository``, ``PasswordHasher``, ``TokenProvider``,
``Clock``, ``IdGenerator``, ``UnitOfWork``.

Critères d'acceptation
----------------------

#. Chaque port est un ``Protocol`` ``@runtime_checkable`` avec signatures typées.
#. Les signatures sont **homogènes** (toutes synchrones) et documentées en RST.
#. ``isinstance(impl, Port)`` fonctionne par duck typing structurel sans héritage
   explicite.
#. Les ports ne dépendent d'aucune implémentation concrète.

Tâches (suivies dans ``docs/backlog/``)
---------------------------------------

* ``TASK-010.6.1`` Définir chaque protocole (1 protocole = 1 fichier).
* ``TASK-010.6.2`` Documenter les signatures (guide ``ports.rst``).
* ``TASK-010.6.3`` Couvrir la conformité structurelle par des tests.
