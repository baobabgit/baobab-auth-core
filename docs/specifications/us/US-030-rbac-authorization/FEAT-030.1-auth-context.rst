FEAT-030.1 — Stabiliser AuthContext
===================================

:Rattachée à: :ref:`us-030`
:Backlog: ``BL-030-001``
:Statut: Ready

Description
-----------

Créer un ``AuthContext`` applicatif immutable, sans secret, exposant les rôles et
permissions agrégés d'un sujet authentifié.

Critères d'acceptation
----------------------

#. Le contexte contient ``auth_subject``, ``user_id``, ``session_id``, ``roles``,
   ``permissions`` et ``authenticated_at``.
#. Les rôles et permissions sont dédupliqués tout en gardant un ordre stable.
#. Les méthodes ``has_role``, ``has_any_role``, ``has_permission``,
   ``has_any_permission`` et ``has_all_permissions`` sont disponibles.
#. Le contexte est immutable et ne contient aucun secret.
