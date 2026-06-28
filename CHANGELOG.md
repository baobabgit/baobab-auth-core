# Changelog

Toutes les modifications notables de ce projet sont documentées ici.

Le format suit [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [Non publié]

### Modifié (évolution du template — nouveau cahier des charges)

- **Gestionnaire de dépendances** : migration de `pip`/`venv` vers `uv` ; `uv.lock`
  versionné pour des builds reproductibles ; `.python-version` figée à `3.13`.
- **Python minimum** : `>=3.11` → `>=3.13` ; CI et mypy mis à jour en conséquence.
- **Couverture minimale** : `90 %` → `95 %` dans `pyproject.toml`, `Makefile`, CI et
  hook `pre-commit`.
- **Formatage + lint séparés** : `ruff format` remplacé par `black` (format) ; `ruff`
  conservé pour le lint uniquement. Pre-commit mis à jour (hook `black` ajouté, hook
  `ruff-format` supprimé).
- **Trois workflows CI** : `ci.yml` restructuré (jobs `quality`, `typing`, `security`,
  `tests`, `commit-policy`, `build` via `uv`) ; `integration.yml` créé (déclenché sur
  les PR vers `version/**`, conditionnel selon `integration_required`) ; `release.yml`
  simplifié (ne réexécute pas la CI, vérifie tag + CHANGELOG, publie via Trusted
  Publishing OIDC).
- **Modèle Git à 3 niveaux** : `main → version/vX.Y.Z → bl/XXX` (suppression des
  branches `us/` et `feat/` qui étaient des branches Git — désormais regroupements
  logiques dans les `status.yaml`).
- **Versionnage statique** : `hatch-vcs` supprimé ; version `0.1.0` déclarée
  statiquement dans `pyproject.toml`.
- **SemVer sans borne supérieure** : le template accompagne une librairie de `v0.1.0`
  vers `v1.0.0` et au-delà.
- **AGENTS.md** refonte complète : ajout des sections uv, tests `tests/unit/`,
  modèle Git 3 niveaux, verrou, recovery, versions, intégrations, SemVer.
- **CLAUDE.md** : références mises à jour (`tests/unit/`, `make all`, verrou, règle
  anti-attribution).
- `.cursor/rules/000-core.mdc` : aligné sur les nouvelles règles.
- `Makefile` : cibles `quality`, `test`, `build`, `all` via `uv run`.
- `noxfile.py` : sessions `quality`, `tests`, `build`, `all` créées.

### Ajouté

- `scripts/check_no_ai_attribution.py` : hook `commit-msg` et outil CI rejetant toute
  attribution interdite dans les messages de commit.
- `.codex/rules/default.rules` : règles Codex (`uv run *` autorisé, `rm -rf` interdit,
  `git push`/`git tag` à confirmer).
- `.python-version` : fixe Python 3.13 pour uv et les outils.
- `uv.lock` : lockfile reproductible.
- `noxfile.py` : sessions qualité/tests/build.
- `docs/ai_workflow/` : structure complète (workflow.md, state/lock.yaml,
  state/queue.yaml, state/dependency_graph.yaml, runs/, roles/, versions/, priorities/).
- `docs/backlog/` : structure (user_stories/, features/, backlogs/).
- `docs/contracts/` : contrats publics (public_api.md, imports.md, exceptions.md,
  models.md, services.md, compatibility.md).
- `docs/integrations/` : compatibility_matrix.yaml + reports/.
- `docs/architecture/adr/` : dossier pour les Architecture Decision Records.
- `tests/unit/` : les tests exemple déplacés depuis `tests/example_package/`.
- `tests/integration/`, `tests/contracts/`, `tests/fixtures/` : nouveaux dossiers.
- `.github/workflows/integration.yml` : workflow d'intégration inter-librairies.
- Badges README : `integration` et `release` ajoutés ; badges simplifiés à 3 workflows.

### Supprimé

- `pip-audit` : retiré des dépendances de dev (non mentionné dans le nouveau CDC).
- Version dérivée du tag git (`hatch-vcs`) : remplacée par versionnage statique.

### Modifié (suite changelog existant)
- Retours du premier dogfood : `init.md` pointe vers `SETUP.md`, étape d'adaptation des
  métadonnées au CDC, réécriture de l'intro README à l'étape PO, décision explicite sur les
  placeholders, et badge Read the Docs neutralisé par défaut.
- Règle « 1 classe = 1 fichier » : dérogation documentée pour les hiérarchies d'exceptions
  (sous-package `exceptions/` par catégorie).
- `scripts/setup_github.sh` : configuration GitHub idempotente (labels, ruleset de
  protection, environnements), tolérante au plan, câblée dans le bootstrap. `SETUP.md` §4
  corrigé (pas d'approbation de PR en mode solo ; protection indisponible en privé/Free).
- Roadmap : champs Date `Début`/`Fin` du Project (gratuits), renseignés aux transitions
  (In progress → Début, Done → Fin) ; documenté dans `gates.md` et le bootstrap.
- Ruff : règle `D401` (imperative mood, heuristique anglaise) désactivée — inadaptée aux
  docstrings françaises.
- Stratégie de branches documentée : trunk-based en v1, modèle imbriqué
  `TASK→FEAT→US→main` réservé à la v2 concurrence.
- Règle « fermeture au merge » (U3) : une issue ne se ferme qu'après le merge de sa PR
  sur `main` — évite les issues « closes mais non livrées » (incident dogfood).

### Ajouté
- Structure initiale du template (règles multi-IA, docs Sphinx, CI, exemples).
- Workflow multi-IA : `docs/workflow/` (rôles, gates, handoff, prompts init/orchestration).
- Sécurité de base : `bandit`, `pip-audit`, Dependabot, `SECURITY.md`.
- Dossier d'intake `docs/specifications/cahier-des-charges/` et champ `:origin:`.
- Contrat d'API publique (`__all__`) avec règle de bump majeur sur rupture.
- CI réorganisée en jobs (lint, type, security, docs, test matriciel) avec concurrency.
- Pipeline de release `release.yml` : tag `v*` → PyPI public (OIDC) + Release GitHub.
- Version dérivée du tag git via `hatch-vcs` (le tag est l'unique source de version).
- Snapshots CI : Bandit en SARIF (onglet Security), job `build` de validation packaging,
  artefacts couverture HTML + JUnit + doc HTML.
- SBOM CycloneDX (via `pip-audit`) attaché aux Releases.
- Durcissement release : TestPyPI sur pré-releases (`vX.Y.Zrc1`), attestation de
  provenance (supply chain), upload SARIF tolérant (repo privé sans GHAS).
- `docs/workflow/SETUP.md` : checklist de configuration GitHub one-time (commandes `gh`).

## [0.4.1] - 2026-06-28

### Corrigé

- **Republication packaging** : la version `0.4.0` ne peut pas être publiée sur
  PyPI car ce nom de fichier y a déjà été utilisé puis supprimé (PyPI interdit
  définitivement la réutilisation, cf. *file-name-reuse*). `0.4.1` republie le
  **même code** que `0.4.0` sous un numéro de version disponible. Aucun
  changement fonctionnel.

## [0.4.0] - 2026-06-28

### Ajouté

- **`DefaultAuthCatalog`** (`domain/catalogs/`, exporté depuis `baobab_auth_core`) :
  catalogue système déterministe de 10 permissions `auth:*`, 4 rôles système
  (USER, ADMIN, SERVICE, SUPER_ADMIN) et leur mapping rôle → permissions. Aucune
  I/O ni variable d'environnement (ADR-0010).
- **Règles strictes `SUPER_ADMIN`** : `AssignRole` refuse l'attribution de
  `SUPER_ADMIN` par un acteur non `SUPER_ADMIN` ; `RemoveRole` refuse le retrait
  de `SUPER_ADMIN` par un acteur non `SUPER_ADMIN` puis protège le dernier
  `SUPER_ADMIN` (`LastSuperAdminRoleRemovalError`).
- **`RolePolicy`** enrichie : `is_super_admin_role`, `can_assign_role(actor_roles,
  role)`, `can_remove_role(actor_roles, role)`, `permits_last_super_admin_removal`
  (ADR-0011).
- **Audit** : nouveaux événements `JWK_ROTATION_REQUESTED` (CRITICAL) et
  `ALL_SESSIONS_REVOKED` (WARNING).
- **`RequestJwkRotation`** : cas d'usage réservé `SUPER_ADMIN` émettant
  `JWK_ROTATION_REQUESTED`.
- **`ChangePassword`** (durci) : ancien vérifié, nouveau validé et différent,
  hachage via port, révocation des autres sessions selon la policy, audit
  `PASSWORD_CHANGED` sans secret (ADR-0012).
- **`RevokeAllSessions`** (durci) : un utilisateur révoque ses sessions, un
  `ADMIN` celles d'un compte standard, protection d'un `SUPER_ADMIN` contre une
  neutralisation abusive ; audit `ALL_SESSIONS_REVOKED` avec `count` (ADR-0012).
- **Test d'architecture** `tests/architecture/` : garantit l'absence de
  dépendance d'infrastructure (FastAPI, SQLAlchemy, JWT, Argon2, bcrypt, httpx,
  requests, `os.environ`, `open`, socket…) dans `src/`.
- Guides : `docs/guides/catalog.rst`, `docs/guides/integration_contracts.rst`.

### Modifié — évolution de contrat (pré-1.0)

- `RolePolicy.can_remove_role` change de signature (`actor_roles, role`) ;
  l'ancienne logique de protection du dernier super-admin est renommée
  `permits_last_super_admin_removal`.
- `DefaultAuthCatalog` exporté dans `baobab_auth_core.__all__`.

### Notes

- `ChangePassword`/`RevokeAllSessions` étaient listés en précondition du cahier
  v0.4.0 mais inexistants : créés ici (ADR-0012).
- 387 tests unitaires, couverture 99 %. Core toujours **pur** (aucune dépendance
  de production).

## [0.3.0] - 2026-06-28

### Ajouté

- **Autorisation RBAC** (couche `application/`) :
  `AuthContext`, `AuthorizationService`, cas d'usage `AssignRole` et `RemoveRole`.
- **Commandes** : `AssignRoleCommand`, `RemoveRoleCommand`.
- **Politique** : `PermissionPolicy` ; extension de `RolePolicy` pour les rôles
  système et la protection du dernier `SUPER_ADMIN`.
- **Ports** : `PermissionRepository`, `RoleRepository` finalisés ; fakes
  `InMemoryPermissionRepository`, `InMemoryRoleRepository`.
- **Audit RBAC** : `ROLE_ASSIGNED`, `ROLE_REMOVED` (sans fuite de secret).
- **Exceptions RBAC** stabilisées : `RoleError`, `LastSuperAdminRoleRemovalError`,
  alias rétrocompatible `LastAdminRoleRemovalError`.
- **Guide** : `docs/guides/rbac.rst`.
- **Tests** : 339 tests unitaires, couverture 99 % (dont `test_rbac_audit.py`).

### Modifié — évolution de contrat (MINOR)

- Export public de `AuthContext`, `AuthorizationService`, `PermissionPolicy`.
- `Logout` et `RevokeSession` peuvent s'appuyer sur `AuthorizationService` pour
  les contrôles d'autorisation fins (ADR-0008).

### Notes

- Le core reste une librairie **pure** : aucune dépendance de production ajoutée.
- `integration_required: false` pour cette version (pas de consommateur bloquant).

## [0.2.0] - 2026-06-28

### Ajouté

- **Cas d'usage d'authentification** (couche `application/use_cases/`) :
  `RegisterUser`, `AuthenticateUser`, `RefreshSession`, `Logout`, `RevokeSession`.
- **Lockout minimal** : verrouillage du compte après `max_failed_login_attempts`
  échecs, auto-déverrouillage après `lockout_duration_seconds`, audit
  `ACCOUNT_LOCKED`.
- **Commandes** (`application/commands/`) : `RegisterUserCommand`,
  `AuthenticateUserCommand`, `RefreshSessionCommand`, `LogoutCommand`,
  `RevokeSessionCommand`.
- **DTO** (`application/results/`) : `AuthenticatedUser`, `TokenPair` (repr
  masquant les tokens), `TokenClaims`, `SessionDTO` (sans refresh token brut),
  et les résultats `RegisterUserResult`, `AuthenticateUserResult`,
  `RefreshSessionResult`.
- **Services applicatifs** : `TokenIssuer` (émission de paire access/refresh) et
  `AuditRecorder` (audit centralisé) ; **`AuditMetadataGuard`** (domaine) qui
  rejette toute métadonnée d'audit sensible (anti-fuite de secret).
- **Entité `Session`** : comportement métier `is_active`, `is_expired`,
  `mark_used`, `rotate_refresh_token`, `revoke` (idempotent), `expire`.
- **Audit auth/session** : `USER_REGISTERED`, `LOGIN_SUCCESS`, `LOGIN_FAILURE`,
  `ACCOUNT_LOCKED`, `SESSION_REFRESHED`, `LOGOUT`, `SESSION_REVOKED`.
- **Guides** : `docs/guides/authentication.rst`, `sessions.rst`, `audit.rst`,
  `security_rules.rst`.
- **Tests** : 290 tests unitaires, couverture 99 % (dont un test de sécurité
  vérifiant l'absence de fuite de secret dans l'audit).

### Modifié — évolution de contrat (MINOR)

- **Port `TokenProvider`** étendu (ADR-0007) : ajout de `create_refresh_token`,
  `verify_refresh_token` et `revoke_token` (refresh tokens et révocation). Le
  `FakeTokenProvider` est étendu en conséquence. Le refresh token brut n'est
  jamais stocké ni audité (seul son `refresh_token_id` est persisté).
- **Port `SessionRepository`** : ajout de `get_by_refresh_token_id` pour
  retrouver une session lors du rafraîchissement.

### Notes

- `AuthContext` complet et contrôles d'autorisation fins reportés à v0.3.0
  (ADR-0008) ; `RevokeSession` accepte un acteur minimal en v0.2.0.
- Le core reste une librairie **pure** : aucune dépendance de production ajoutée.

## [0.1.0] - 2026-06-26

### Ajouté

- **Exceptions** hiérarchisées en 6 familles (`base`, `validation`, `user`, `auth`,
  `session`, `role`, `authorization`) ; tout réexporté depuis `baobab_auth_core.exceptions`.
- **Value objects** (frozen dataclasses) : `Email`, `AuthSubject`, `PlainPassword`,
  `PasswordHash`, `RoleName`, `PermissionName`, `UserId`, `RoleId`, `PermissionId`,
  `SessionId`, `TokenId`, `AuditEventId`. Masquage automatique des secrets dans
  `__str__`/`__repr__`, normalisation (minuscules/majuscules), validation format.
- **Entités** (dataclasses avec comportement métier) : `User` (méthodes `activate`,
  `disable`, `lock`, `unlock`, `assign_role`, `remove_role`, `mark_login_failure`, …),
  `Role`, `Permission`, `Session`, `AuditEvent` (immuable), `UserProfile`.
- **Enums** (`StrEnum`) : `UserStatus` (PENDING/ACTIVE/LOCKED/DISABLED/DELETED),
  `SessionStatus` (ACTIVE/REVOKED/EXPIRED), `AuditSeverity` (INFO/WARNING/CRITICAL),
  `AuditEventType` (12 types d'événements).
- **Politiques métier** (frozen dataclasses injectables) : `PasswordPolicy` (longueur,
  complexité, interdiction e-mail), `SessionPolicy` (TTL tokens, verrouillage),
  `RolePolicy` (rôle par défaut, protection dernier super-admin).
- **Ports** (`typing.Protocol`, `@runtime_checkable`) : `Clock`, `IdGenerator`,
  `PasswordHasher`, `TokenProvider`, `UserRepository`, `RoleRepository`,
  `PermissionRepository`, `SessionRepository`, `AuditRepository`, `UnitOfWork`.
- **Fakes** testables : `FakeClock` (avance dans le temps), `FakeIdGenerator`
  (séquence prévisible), `FakePasswordHasher` (`hashed:<val>`), `FakeTokenProvider`
  (markers `EXPIRED`/`INVALID`), repositories en mémoire pour les 5 ports,
  `InMemoryUnitOfWork` (suivi committed/rolled_back).
- **Tests** : 234 tests unitaires, couverture 98.89 %, arborescence miroir complète.
- Documentation guides : `docs/guides/domain_model.rst`, `docs/guides/ports.rst`,
  `docs/guides/testing.rst`.

### Notes techniques

- Librairie **pure** : zéro dépendance de production (pas de FastAPI, SQLAlchemy,
  JWT, Argon2, bcrypt, httpx, Docker).
- Python ≥ 3.13 requis (`StrEnum`, `datetime.UTC`, `dataclasses.FrozenInstanceError`).
- Architecture hexagonale : `domain/` (value objects, entités, politiques, enums),
  `ports/` (protocoles), `testing/` (fakes + repositories en mémoire).
