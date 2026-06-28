FEAT-030.6 — Stabiliser exceptions RBAC
=======================================

:Rattachée à: :ref:`us-030`
:Backlog: ``BL-030-006``
:Statut: DONE

Description
-----------

Stabiliser les exceptions publiques liées à l'autorisation, aux rôles et aux
permissions.

Critères d'acceptation
----------------------

#. Les exceptions ``AuthorizationError``, ``ForbiddenError``,
   ``PermissionDeniedError`` et ``RoleError`` existent.
#. Les exceptions ``RoleNotFoundError``, ``PermissionNotFoundError`` et
   ``LastSuperAdminRoleRemovalError`` existent.
#. L'alias ``LastAdminRoleRemovalError`` est fourni si un ancien symbole existe.
#. Les exports publics et docstrings RST sont à jour.
