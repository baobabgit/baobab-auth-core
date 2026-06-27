FEAT-010.4 — Implémenter enums et policies
==========================================

:Rattachée à: :ref:`us-010`
:Issue GitHub: ``[FEAT-010.4]`` (sub-issue de ``[US-010]``)
:Backlog: ``BL-010-004``
:Statut: Implémentée

Description
-----------

Fournir les énumérations de statut/événement (``StrEnum``) et les policies
métier injectables (frozen dataclasses) configurant le comportement du domaine.

Énumérations livrées
--------------------

* ``UserStatus`` : ``PENDING``, ``ACTIVE``, ``LOCKED``, ``DISABLED``, ``DELETED``.
* ``SessionStatus`` : ``ACTIVE``, ``REVOKED``, ``EXPIRED``.
* ``AuditSeverity`` : ``INFO``, ``WARNING``, ``CRITICAL``.
* ``AuditEventType`` : 12 types (``USER_REGISTERED`` … ``ACCOUNT_DELETED``).

Policies livrées
----------------

* ``PasswordPolicy`` (``min_length=12``, ``max_length=256``, ``require_letter``,
  ``require_digit_or_symbol``, ``forbid_email_as_password``).
* ``SessionPolicy`` (``access_token_ttl_seconds=900``,
  ``refresh_token_ttl_seconds=2592000``, ``max_failed_login_attempts=5``,
  ``lockout_duration_seconds=900``, ``revoke_other_sessions_on_password_change``).
* ``RolePolicy`` (``default_role_name=USER``, ``super_admin_role_name=SUPER_ADMIN``,
  ``enforce_last_super_admin``).

Critères d'acceptation
----------------------

#. Toutes les enums héritent de ``StrEnum`` et sérialisent en chaîne.
#. ``PasswordPolicy.validate`` lève ``WeakPasswordError`` si la règle n'est pas
   respectée.
#. ``RolePolicy`` avec ``enforce_last_super_admin`` empêche la suppression du
   dernier super-admin (``LastSuperAdminRoleRemovalError``).
#. Les valeurs par défaut sont conformes au cahier des charges (§7).

Tâches (suivies dans ``docs/backlog/``)
---------------------------------------

* ``TASK-010.4.1`` Implémenter les enums.
* ``TASK-010.4.2`` Implémenter les policies et leurs validations.
* ``TASK-010.4.3`` Couvrir valeurs par défaut et validations par des tests.
