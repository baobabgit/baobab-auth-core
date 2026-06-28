Codes d'erreur métier (v0.5.0)
==============================

Chaque exception publique expose ``error_code`` (code applicatif stable),
``safe_message`` (message client sans secret) et ``http_status`` (statut HTTP
**recommandé**, jamais une ``HTTPException``). Voir :doc:`../architecture/adr/0013-error-codes-metier`.

.. list-table::
   :header-rows: 1
   :widths: 38 40 12

   * - Exception
     - ``error_code``
     - HTTP
   * - ``InvalidCredentialsError``
     - ``auth.credentials.invalid``
     - 401
   * - ``TokenInvalidError`` / ``TokenExpiredError``
     - ``auth.token.invalid`` / ``auth.token.expired``
     - 401
   * - ``ForbiddenError``
     - ``auth.authorization.forbidden``
     - 403
   * - ``PermissionDeniedError``
     - ``auth.authorization.permission_denied``
     - 403
   * - ``UserNotFoundError``
     - ``auth.user.not_found``
     - 404
   * - ``UserDisabledError``
     - ``auth.user.disabled``
     - 403
   * - ``UserAlreadyExistsError``
     - ``auth.user.already_exists``
     - 409
   * - ``LastSuperAdminRoleRemovalError``
     - ``auth.role.last_super_admin``
     - 409
   * - ``UserLockedError``
     - ``auth.user.locked``
     - 423
   * - ``RoleNotFoundError`` / ``PermissionNotFoundError``
     - ``auth.role.not_found`` / ``auth.permission.not_found``
     - 404
   * - ``ValidationError`` (et dérivées)
     - ``auth.validation.*``
     - 400

Le message détaillé (logs internes) reste disponible via ``str(exc)`` /
``exc.message`` ; ``safe_message`` est la version publique.
