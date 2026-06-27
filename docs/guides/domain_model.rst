Modèle de domaine
=================

.. spec: BL-010-002, BL-010-003, BL-010-004

Cette page décrit les briques métier de ``baobab-auth-core`` :
value objects, entités, enums et politiques.

Value Objects
-------------

Les value objects sont des **frozen dataclasses** : immuables, comparables par valeur,
jamais par identité. Ils normalisent et valident leur contenu à la construction.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Classe
     - Description
   * - ``Email``
     - Normalise en minuscules ; exige la présence d'un ``@``.
   * - ``AuthSubject``
     - Identifiant de sujet d'authentification (non vide, non blanc).
   * - ``PlainPassword``
     - Mot de passe en clair. ``__str__`` et ``__repr__`` retournent ``"***"``.
   * - ``PasswordHash``
     - Hash de mot de passe opaque. Même masquage que ``PlainPassword``.
   * - ``RoleName``
     - Normalise en majuscules ; refuse les espaces.
   * - ``PermissionName``
     - Format ``scope:resource:action`` (3 segments non vides séparés par ``:``)
   * - ``UserId``, ``RoleId``, ``PermissionId``, ``SessionId``, ``TokenId``, ``AuditEventId``
     - Identifiants typés (non vides, non blancs).

Utilisation::

    from baobab_auth_core.domain.value_objects.email import Email
    from baobab_auth_core.domain.value_objects.permission_name import PermissionName

    email = Email("Alice@Example.COM")   # "alice@example.com"
    perm = PermissionName("users:profile:read")

Enums
-----

Toutes les enums héritent de ``StrEnum`` (Python 3.11+) afin de sérialiser
directement en chaîne de caractères.

``UserStatus``
~~~~~~~~~~~~~~

Cycle de vie d'un compte utilisateur :
``PENDING`` → ``ACTIVE`` → ``LOCKED`` / ``DISABLED`` → ``DELETED``.

``SessionStatus``
~~~~~~~~~~~~~~~~~

État d'une session : ``ACTIVE``, ``REVOKED``, ``EXPIRED``.

``AuditSeverity``
~~~~~~~~~~~~~~~~~

Niveau de criticité d'un événement d'audit : ``INFO``, ``WARNING``, ``CRITICAL``.

``AuditEventType``
~~~~~~~~~~~~~~~~~~

Catalogue des 12 types d'événements traçables :
``USER_REGISTERED``, ``LOGIN_SUCCESS``, ``LOGIN_FAILURE``, ``LOGOUT``,
``SESSION_REFRESHED``, ``SESSION_REVOKED``, ``ROLE_ASSIGNED``, ``ROLE_REMOVED``,
``PASSWORD_CHANGED``, ``ACCOUNT_LOCKED``, ``ACCOUNT_DISABLED``, ``ACCOUNT_DELETED``.

Entités
-------

Les entités sont des **dataclasses mutables** portant l'identité et le comportement
métier. Elles n'ont pas accès à la persistance — c'est le rôle des ports.

``User``
~~~~~~~~

Champs principaux : ``id``, ``email``, ``password_hash``, ``status``, ``roles``,
``failed_login_count``, ``created_at``, ``updated_at``.

Méthodes métier :

- ``activate()`` / ``disable()`` / ``lock()`` / ``unlock()`` — transitions de statut.
- ``mark_login_success()`` / ``mark_login_failure()`` — gestion des échecs.
- ``change_password_hash(new_hash)`` — changement de mot de passe.
- ``assign_role(role_name)`` / ``remove_role(role_name)`` / ``has_role(role_name)``
  — gestion des rôles.

Invariants vérifiés à la construction (``__post_init__``) :

- ``failed_login_count >= 0``
- Pas de rôle en doublon dans la liste ``roles``.

``Role``
~~~~~~~~

Champs : ``id``, ``name`` (``RoleName``), ``permission_names``
(``tuple[PermissionName, ...]``), ``is_system``, ``created_at``.

``Permission``
~~~~~~~~~~~~~~

Champs : ``id``, ``name`` (``PermissionName``), ``resource``, ``action``,
``is_system``, ``created_at``.

``Session``
~~~~~~~~~~~

Champs : ``id``, ``user_id``, ``token_id``, ``status``, ``created_at``,
``expires_at`` ; champs optionnels ``refresh_token_id``, ``refresh_expires_at``,
``revoked_at``.

``AuditEvent``
~~~~~~~~~~~~~~

**Frozen dataclass** (événement immuable) : ``id``, ``user_id``, ``event_type``,
``severity``, ``occurred_at``, ``metadata`` (``Mapping[str, Any]``).

``UserProfile``
~~~~~~~~~~~~~~~

Vue publique sans secrets : ``user_id``, ``email``, ``status``, ``roles``,
``created_at``.

Politiques métier
-----------------

Les politiques sont des **frozen dataclasses injectables** configurant le comportement
du domaine sans accès à la persistance.

``PasswordPolicy``
~~~~~~~~~~~~~~~~~~

Paramètres (avec valeurs par défaut) :

- ``min_length = 12``, ``max_length = 256``
- ``require_letter = True``
- ``require_digit_or_symbol = True``
- ``forbid_email_as_password = True``

Méthode ``validate(password, email=None)`` — lève ``WeakPasswordError`` si la
politique n'est pas respectée.

``SessionPolicy``
~~~~~~~~~~~~~~~~~

Paramètres :

- ``access_token_ttl_seconds = 900`` (15 min)
- ``refresh_token_ttl_seconds = 2592000`` (30 jours)
- ``max_failed_login_attempts = 5``
- ``lockout_duration_seconds = 900``
- ``revoke_other_sessions_on_password_change = True``

``RolePolicy``
~~~~~~~~~~~~~~

Paramètres :

- ``default_role_name = RoleName("USER")``
- ``super_admin_role_name = RoleName("SUPER_ADMIN")``
- ``enforce_last_super_admin = True`` — empêche la suppression du dernier
  super-admin (lève ``LastSuperAdminRoleRemovalError``).
