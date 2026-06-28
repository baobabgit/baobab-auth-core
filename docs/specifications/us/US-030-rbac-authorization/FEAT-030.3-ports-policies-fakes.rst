FEAT-030.3 — Finaliser ports, policies et fakes RBAC
====================================================

:Rattachée à: :ref:`us-030`
:Backlog: ``BL-030-003``
:Statut: TODO

Description
-----------

Finaliser les ports de repository RBAC, renforcer les policies et compléter les
fakes in-memory utiles aux tests.

Critères d'acceptation
----------------------

#. ``RoleRepository`` expose ``get_by_name``, ``list_roles``, ``save`` et
   ``count_users_with_role``.
#. ``PermissionRepository`` expose ``get_by_name``, ``list_permissions`` et ``save``.
#. ``RolePolicy`` protège le dernier ``SUPER_ADMIN``.
#. ``PermissionPolicy`` valide le format ``scope:resource:action``.
#. Les repositories in-memory RBAC sont déterministes.
