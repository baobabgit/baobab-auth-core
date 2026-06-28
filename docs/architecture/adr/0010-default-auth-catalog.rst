ADR-0010 — Catalogue d'autorisation par défaut (``DefaultAuthCatalog``)
======================================================================

:Statut: Accepté
:Date: 2026-06-28
:Version: v0.4.0
:Backlogs: BL-040-001 → BL-040-004

Contexte
--------

La v0.4.0 doit fournir un catalogue **système** stable : 4 rôles, 10 permissions
``auth:*`` et leur mapping. Ce catalogue est un **contrat** consommé par les
projets parents pour amorcer leur RBAC, sans base de données ni variable
d'environnement.

Décision
--------

Introduire ``baobab_auth_core.domain.catalogs.DefaultAuthCatalog`` exposant :

- ``permissions() -> tuple[Permission, ...]`` (ordre déterministe) ;
- ``roles() -> tuple[Role, ...]`` ;
- ``role_permissions() -> Mapping[RoleName, tuple[PermissionName, ...]]``.

Le catalogue est **codé en dur** dans le domaine (aucune I/O), avec des
collections immuables. Il est exporté depuis ``baobab_auth_core.__init__`` (contrat
public). Les permissions système portent ``is_system=True``.

Conséquences
------------

- Le mapping rôle → permissions devient une **référence contractuelle** versionnée
  (toute rupture impose un bump majeur + note de migration).
- Le core reste pur : le catalogue ne dépend d'aucune infrastructure.
- Les projets parents peuvent étendre/écraser le catalogue côté hôte sans modifier
  le core.
