FEAT-010.7 — Implémenter les fakes in-memory
============================================

:Rattachée à: :ref:`us-010`
:Issue GitHub: ``[FEAT-010.7]`` (sub-issue de ``[US-010]``)
:Backlog: ``BL-010-007``
:Statut: Implémentée

Description
-----------

Fournir, dans le sous-package ``baobab_auth_core.testing``, une implémentation de
test pour chaque port, afin d'écrire des tests déterministes sans dépendance
externe. Ces fakes font partie du livrable (et non des tests internes).

Fakes livrés
-----------

* ``FakeClock`` — horloge contrôlable (``set_now``, ``advance``).
* ``FakeIdGenerator`` — identifiants prévisibles ``"<préfixe>-<n>"``.
* ``FakePasswordHasher`` — hachage simulé par préfixe ``"hashed:"``.
* ``FakeTokenProvider`` — tokens ``"fake-token:<subject>"`` avec markers d'erreur.
* ``InMemoryUserRepository``, ``InMemoryRoleRepository``,
  ``InMemoryPermissionRepository``, ``InMemorySessionRepository``,
  ``InMemoryAuditRepository``.
* ``InMemoryUnitOfWork`` — suit ``commit``/``rollback``.

Critères d'acceptation
----------------------

#. Chaque fake satisfait ``isinstance(fake, Port)`` du port correspondant.
#. Les repositories en mémoire exposent une réinitialisation (``clear``).
#. ``FakeTokenProvider`` simule l'expiration et l'invalidité via markers
   (``EXPIRED``/``INVALID``) levant les exceptions adéquates.
#. Aucun fake n'effectue de cryptographie ni d'accès réseau/fichier réels.

Tâches (suivies dans ``docs/backlog/``)
---------------------------------------

* ``TASK-010.7.1`` Implémenter chaque fake (1 classe = 1 fichier).
* ``TASK-010.7.2`` Couvrir chaque fake par des tests.
