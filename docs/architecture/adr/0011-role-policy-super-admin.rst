ADR-0011 — ``RolePolicy`` renforcée et règles strictes ``SUPER_ADMIN``
=====================================================================

:Statut: Accepté
:Date: 2026-06-28
:Version: v0.4.0
:Backlogs: BL-040-005, BL-040-006, BL-040-007

Contexte
--------

La v0.3.0 fournit ``RolePolicy.can_remove_role(role_name, users_with_role)`` qui
protège le **dernier** ``SUPER_ADMIN`` (contrôle de cardinalité). La v0.4.0 exige
en plus un contrôle d'**autorisation de l'acteur** (§8/§9) : seul un
``SUPER_ADMIN`` peut attribuer ou retirer le rôle ``SUPER_ADMIN``. Le cahier §9
nomme ``can_assign_role(actor_roles, role)`` et ``can_remove_role(actor_roles,
role)`` — ce dernier entre en collision de signature avec la méthode existante.

Décision
--------

Distinguer les deux préoccupations dans ``RolePolicy`` :

- ``is_super_admin_role(role) -> bool`` ;
- ``can_assign_role(actor_roles, role) -> bool`` — autorisation d'attribution ;
- ``can_remove_role(actor_roles, role) -> bool`` — autorisation de retrait
  (remplace la signature v0.3.0) ;
- ``permits_last_super_admin_removal(role, users_with_role) -> bool`` — protection
  de cardinalité (logique historique, renommée).

``AssignRole`` refuse l'attribution de ``SUPER_ADMIN`` via ``can_assign_role`` ;
``RemoveRole`` refuse le retrait via ``can_remove_role`` puis vérifie
``permits_last_super_admin_removal``.

Conséquences
------------

- **Changement de contrat** (pré-1.0) : la signature de ``can_remove_role`` change
  et une méthode est renommée ; documenté au CHANGELOG.
- Séparation claire « qui a le droit » (autorisation) vs « combien il en reste »
  (cardinalité), chacune testable indépendamment.
