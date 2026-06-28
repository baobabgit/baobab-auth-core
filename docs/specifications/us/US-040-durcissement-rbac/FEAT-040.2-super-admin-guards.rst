FEAT-040.2 — Règles strictes SUPER_ADMIN
========================================

:Rattachée à: :ref:`us-040`
:Statut: Implémentée

Description
-----------

Durcissement de ``AssignRole``/``RemoveRole`` et de ``RolePolicy`` autour du rôle ``SUPER_ADMIN``.

Critères d'acceptation
----------------------

#. Un acteur non ``SUPER_ADMIN`` ne peut ni attribuer ni retirer ``SUPER_ADMIN`` (``ForbiddenError``).
#. Le dernier ``SUPER_ADMIN`` est protégé (``LastSuperAdminRoleRemovalError``).
#. ``RolePolicy`` expose ``is_super_admin_role``, ``can_assign_role``, ``can_remove_role``.
