FEAT-030.2 — Implémenter AuthorizationService
=============================================

:Rattachée à: :ref:`us-030`
:Backlog: ``BL-030-002``
:Statut: TODO

Description
-----------

Construire le service applicatif d'autorisation chargé d'agréger les rôles et
permissions puis d'exiger un rôle ou une permission.

Critères d'acceptation
----------------------

#. ``build_context(auth_subject)`` charge l'utilisateur et ses rôles via les ports.
#. Les permissions des rôles connus sont agrégées et dédupliquées.
#. Les rôles inconnus sont ignorés en v0.3.0 et ce choix est testé.
#. ``require_role`` et ``require_permission`` lèvent des exceptions métier stables.
