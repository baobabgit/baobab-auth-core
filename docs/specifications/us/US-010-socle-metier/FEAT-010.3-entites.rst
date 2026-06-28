FEAT-010.3 — Implémenter les entités
====================================

:Rattachée à: :ref:`us-010`
:Issue GitHub: ``[FEAT-010.3]`` (sub-issue de ``[US-010]``)
:Backlog: ``BL-010-003``
:Statut: Implémentée

Description
-----------

Fournir les entités métier portant l'identité et le comportement, sans accès à la
persistance (c'est le rôle des ports).

Entités livrées
---------------

``User``, ``UserProfile``, ``Role``, ``Permission``, ``Session``, ``AuditEvent``.

Critères d'acceptation
----------------------

#. ``User`` expose les transitions ``activate``, ``disable``, ``lock``,
   ``unlock`` et les méthodes ``mark_login_success``, ``mark_login_failure``,
   ``change_password_hash``, ``assign_role``, ``remove_role``, ``has_role``.
#. Invariants ``User`` vérifiés à la construction : ``email`` normalisé obligatoire,
   ``auth_subject`` stable, ``password_hash`` jamais vide, ``failed_login_count >= 0``,
   dates UTC aware, rôles sans doublon.
#. ``UserProfile`` ne contient aucun secret.
#. ``AuditEvent`` est immuable (frozen dataclass).
#. ``Role``, ``Permission`` et ``Session`` portent les champs définis au cahier des
   charges (§4).

Tâches (suivies dans ``docs/backlog/``)
---------------------------------------

* ``TASK-010.3.1`` Implémenter chaque entité (1 classe = 1 fichier).
* ``TASK-010.3.2`` Implémenter les méthodes métier de ``User``.
* ``TASK-010.3.3`` Couvrir entités et invariants par des tests.
