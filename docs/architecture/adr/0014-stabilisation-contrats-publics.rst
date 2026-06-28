ADR-0014 — Stabilisation des contrats publics et cas d'usage de lecture/admin
============================================================================

:Statut: Accepté
:Date: 2026-06-28
:Version: v0.5.0
:Backlogs: BL-050-001, BL-050-007, BL-050-008, BL-050-009

Contexte
--------

La v0.5.0 prépare l'intégration des briques ``database``, ``security``, ``api``,
``client`` et ``admin`` sans ajouter d'infrastructure au core. Il faut une surface
publique explicite et des cas d'usage de lecture/admin réutilisables.

Décision
--------

- **API publique** : ``baobab_auth_core.__all__`` exporte explicitement entités,
  value objects, enums, policies, ``DefaultAuthCatalog``, ports, DTO et cas
  d'usage. Un test d'import garantit la cohérence.
- **Cas d'usage de lecture** (``GetUserBySubject``, ``GetCurrentUser``,
  ``ListRoles``, ``ListPermissions``, ``ListUserSessions``) : exposent des
  *queries* + résultats DTO sans secret. **Ils n'émettent pas d'audit** : une
  lecture ne modifie aucun état et il n'existe pas d'événement d'audit de lecture
  (décision assumée — l'audit reste réservé aux mutations).
- **Cas d'usage admin** (``DisableUser``, ``EnableUser``, ``BootstrapSuperAdmin``)
  : mutations auditées (``ACCOUNT_DISABLED``, ``ACCOUNT_ENABLED``,
  ``ROLE_ASSIGNED``). ``BootstrapSuperAdmin`` est un **amorçage système** : il
  n'opère que s'il n'existe encore aucun ``SUPER_ADMIN`` (sinon refus), ce qui
  permet de créer le premier super-admin sans acteur super-admin préexistant.
- **Tests contractuels** (``tests/contracts/{database,security,api,client,admin}``)
  : valident la surface publique en n'important **que** ``baobab_auth_core``.

Conséquences
------------

- Ajout de l'événement d'audit ``ACCOUNT_ENABLED``.
- ``AuthenticatedUser`` gagne un champ ``permissions`` (et un accès ``roles``) ;
  rétrocompatible (champ ``role_names`` conservé).
- Le core reste pur : aucune dépendance d'infrastructure n'est introduite.
