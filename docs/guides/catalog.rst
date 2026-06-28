Catalogue d'autorisation par défaut (v0.4.0)
============================================

``DefaultAuthCatalog`` (exporté depuis ``baobab_auth_core``) fournit le socle
système : permissions, rôles et leur mapping, de façon **déterministe** et sans
aucune I/O.

.. code-block:: python

   from baobab_auth_core import DefaultAuthCatalog

   catalog = DefaultAuthCatalog()
   permissions = catalog.permissions()        # 10 permissions auth:*
   roles = catalog.roles()                     # USER, ADMIN, SERVICE, SUPER_ADMIN
   mapping = catalog.role_permissions()        # RoleName -> tuple[PermissionName, ...]

Permissions système
--------------------

``auth:user:read``, ``auth:user:write``, ``auth:user:disable``,
``auth:role:read``, ``auth:role:write``, ``auth:session:read``,
``auth:session:revoke``, ``auth:audit:read``, ``auth:jwk:read``,
``auth:jwk:rotate`` (toutes ``is_system=True``).

Mapping rôle → permissions
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Rôle
     - Permissions
   * - ``USER``
     - ``auth:user:read``, ``auth:session:read``
   * - ``ADMIN``
     - tout sauf ``auth:role:write`` et ``auth:jwk:rotate``
   * - ``SERVICE``
     - aucune
   * - ``SUPER_ADMIN``
     - toutes les permissions ``auth:*``

Règles strictes ``SUPER_ADMIN``
-------------------------------

- Seul un ``SUPER_ADMIN`` peut **attribuer** ou **retirer** le rôle ``SUPER_ADMIN``
  (``AssignRole`` / ``RemoveRole`` → ``ForbiddenError`` sinon).
- Le **dernier** ``SUPER_ADMIN`` est protégé (``LastSuperAdminRoleRemovalError``).
- Seul un ``SUPER_ADMIN`` peut déclencher ``RequestJwkRotation`` (audit
  ``JWK_ROTATION_REQUESTED``, CRITICAL).

Voir aussi :doc:`rbac`, :doc:`security_rules`, :doc:`audit`.
