ADR-0009 — RBAC applicatif pur et AuthContext immutable
=======================================================

:Statut: Accepté
:Date: 2026-06-28
:Spec: US-030 / FEAT-030.1 / FEAT-030.2

Contexte
--------

La version ``0.3.0`` doit stabiliser le RBAC sans introduire de dépendance
technique. Le service d'autorisation doit pouvoir construire un contexte métier
à partir des ports existants et fonctionner dans les tests in-memory.

Décision
--------

Le RBAC reste dans la couche applicative et domaine pur. ``AuthContext`` est un
DTO immutable, sans secret, contenant uniquement l'identité métier, les rôles,
les permissions et la date d'authentification.

``AuthorizationService`` agrège les permissions des rôles connus. En v0.3.0, les
rôles inconnus associés à un utilisateur sont ignorés pendant la construction du
contexte. Cette stratégie suit l'option recommandée du cahier des charges et doit
être testée explicitement.

Conséquences
------------

- Les intégrateurs peuvent utiliser le RBAC sans API HTTP, base de données ou JWT concret.
- Un rôle supprimé ou absent n'empêche pas la construction du contexte.
- Les refus explicites restent portés par ``require_role`` et ``require_permission``.
- Une stratégie stricte ``RoleNotFoundError`` pourra être introduite ultérieurement
  si un besoin de conformité l'exige.
