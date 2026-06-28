Autorisation RBAC (v0.3.0)
==========================

Cette page décrit le parcours RBAC : construction d'un :class:`~baobab_auth_core.application.results.auth_context.AuthContext`,
contrôles d'autorisation, assignation et retrait de rôles.

Contexte d'autorisation — ``AuthContext``
-----------------------------------------

.. code-block:: python

   from baobab_auth_core.application.services.authorization_service import (
       AuthorizationService,
   )

   service = AuthorizationService(users, roles, permissions)
   context = service.build_context("subject-alice")

Le contexte agrège les rôles effectifs de l'utilisateur et **déduplique** les
permissions issues de plusieurs rôles. Les rôles absents du catalogue sont ignorés.

Contrôles fins — ``AuthorizationService``
-------------------------------------------

.. code-block:: python

   from baobab_auth_core.exceptions import ForbiddenError, PermissionDeniedError

   if service.has_role(context, "ADMIN"):
       service.require_role(context, "ADMIN")

   if service.has_permission(context, "auth:user:read"):
       service.require_permission(context, "auth:user:read")

Les refus lèvent respectivement :class:`~baobab_auth_core.exceptions.authorization.ForbiddenError`
(rôle requis absent) ou :class:`~baobab_auth_core.exceptions.authorization.PermissionDeniedError`
(permission requise absente).

Assignation — ``AssignRole``
----------------------------

.. code-block:: python

   from baobab_auth_core.application.commands.assign_role_command import (
       AssignRoleCommand,
   )
   from baobab_auth_core.application.use_cases.assign_role import AssignRole

   use_case = AssignRole(
       users, roles, authorization, audit, id_generator, clock, uow,
   )
   use_case.execute(
       AssignRoleCommand(
           actor_subject="subject-admin",
           target_user_id="user-target",
           role_name="support",
       )
   )

Seuls les acteurs ``ADMIN`` ou ``SUPER_ADMIN`` peuvent assigner un rôle.
L'assignation est **idempotente** (aucun audit si le rôle est déjà présent).
Audit : ``ROLE_ASSIGNED``.

Retrait — ``RemoveRole``
------------------------

.. code-block:: python

   from baobab_auth_core.application.commands.remove_role_command import (
       RemoveRoleCommand,
   )
   from baobab_auth_core.application.use_cases.remove_role import RemoveRole

   use_case = RemoveRole(
       users, roles, authorization, audit, id_generator, clock, uow,
   )
   use_case.execute(
       RemoveRoleCommand(
           actor_subject="subject-admin",
           target_user_id="user-target",
           role_name="support",
       )
   )

Le retrait est **idempotent**. La suppression du rôle ``SUPER_ADMIN`` du
**dernier** super-administrateur est refusée
(``LastSuperAdminRoleRemovalError`` ; alias rétrocompatible
``LastAdminRoleRemovalError``). Audit : ``ROLE_REMOVED``.

Exceptions RBAC
---------------

Les exceptions publiques sont exportées depuis ``baobab_auth_core.exceptions`` :

- ``AuthorizationError``, ``ForbiddenError``, ``PermissionDeniedError``
- ``RoleError``, ``RoleNotFoundError``, ``PermissionNotFoundError``
- ``LastSuperAdminRoleRemovalError``, ``LastAdminRoleRemovalError`` (alias)

Audit sans fuite de secret
--------------------------

Les métadonnées d'audit ``ROLE_ASSIGNED`` et ``ROLE_REMOVED`` ne contiennent
ni mot de passe, ni token, ni hash. Voir aussi :doc:`audit` et
:doc:`security_rules`.
