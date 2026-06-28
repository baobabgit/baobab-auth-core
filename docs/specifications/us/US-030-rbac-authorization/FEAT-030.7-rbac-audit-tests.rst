FEAT-030.7 — Compléter audit et tests RBAC
==========================================

:Rattachée à: :ref:`us-030`
:Backlog: ``BL-030-007``
:Statut: TODO

Description
-----------

Compléter la couverture de tests RBAC et vérifier que les audits RBAC ne
contiennent aucun secret.

Critères d'acceptation
----------------------

#. Les permissions multi-rôles sont agrégées et dédupliquées.
#. Les refus de rôle et permission sont testés.
#. Les assignations et retraits nominaux et idempotents sont testés.
#. La protection du dernier ``SUPER_ADMIN`` est testée.
#. Les audits ``ROLE_ASSIGNED`` et ``ROLE_REMOVED`` ne contiennent ni password,
   ni token, ni secret, ni hash.
