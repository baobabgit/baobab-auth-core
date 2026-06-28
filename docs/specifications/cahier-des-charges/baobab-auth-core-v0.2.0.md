# Cahier des charges — `baobab-auth-core` — Version `0.2.0`

**Projet :** `baobab-auth-core`  
**Type de document :** cahier des charges versionné  
**Destination :** IA de développement  
**Format :** Markdown  
**Règle d'architecture constante :** le core reste une librairie métier pure, sans FastAPI, SQLAlchemy, Alembic, PostgreSQL, JWT concret, Argon2, bcrypt, httpx, requests, Docker ou accès fichier/réseau/env var en production.

---


## 1. Objectif de la version

La version `0.2.0` ajoute le parcours d'authentification et de gestion de session au socle `0.1.0`.

Elle doit permettre :

- d'inscrire un utilisateur ;
- d'authentifier un utilisateur ;
- de créer une session ;
- d'émettre une paire de tokens via un port ;
- de rafraîchir une session ;
- de déconnecter un utilisateur ;
- de révoquer une session ;
- de produire les événements d'audit associés.

Le core ne génère toujours pas de JWT concret et ne hashe pas réellement les mots de passe. Il orchestre les ports `PasswordHasher` et `TokenProvider`.

---

## 2. Préconditions

La version `0.1.0` doit fournir :

```text
User, Session, AuditEvent
Email, Password, PasswordHash, AuthSubject, SessionId, TokenId
PasswordPolicy, SessionPolicy
UserRepository, SessionRepository, AuditRepository
PasswordHasher, TokenProvider, Clock, IdGenerator, UnitOfWork
Fake repositories et fakes techniques
```

---

## 3. Périmètre fonctionnel

La version inclut :

```text
RegisterUser
AuthenticateUser
RefreshSession
Logout
RevokeSession
SessionDTO
TokenPair
TokenClaims
AuthenticationResult
Audit minimal auth/session
Lockout minimal
```

---

## 4. Cas d'usage `RegisterUser`

### 4.1 Commande

```python
@dataclass(frozen=True)
class RegisterUserCommand:
    email: str
    password: str
    display_name: str | None = None
    locale: str | None = None
    timezone: str | None = None
    ip_address: str | None = None
    user_agent: str | None = None
```

### 4.2 Résultat

```python
@dataclass(frozen=True)
class RegisterUserResult:
    user: AuthenticatedUser
```

### 4.3 Règles métier

- normaliser l'email ;
- refuser un email déjà existant ;
- valider le mot de passe ;
- hasher via `PasswordHasher` ;
- générer `UserId` et `AuthSubject` via `IdGenerator` ;
- créer l'utilisateur ;
- attribuer le rôle `USER` si disponible ;
- produire l'audit `USER_REGISTERED` ;
- commit atomique.

### 4.4 Erreurs

```text
InvalidEmailError
WeakPasswordError
UserAlreadyExistsError
```

---

## 5. Cas d'usage `AuthenticateUser`

### 5.1 Commande

```python
@dataclass(frozen=True)
class AuthenticateUserCommand:
    email: str
    password: str
    ip_address: str | None = None
    user_agent: str | None = None
    device_label: str | None = None
```

### 5.2 Résultat

```python
@dataclass(frozen=True)
class AuthenticateUserResult:
    user: AuthenticatedUser
    session: SessionDTO
    tokens: TokenPair
```

### 5.3 Règles

- utiliser un message d'échec générique ;
- ne pas divulguer si l'email existe ;
- vérifier le mot de passe via `PasswordHasher` ;
- refuser un compte `DISABLED`, `DELETED`, `LOCKED` ;
- incrémenter les échecs de connexion ;
- verrouiller après `max_failed_login_attempts` ;
- réinitialiser les échecs en cas de succès ;
- créer une session active ;
- générer un `refresh_token_id` ;
- émettre une paire de tokens via `TokenProvider` ;
- produire `LOGIN_SUCCESS` ou `LOGIN_FAILURE` ;
- produire `ACCOUNT_LOCKED` si seuil atteint ;
- commit atomique.

---

## 6. Cas d'usage `RefreshSession`

### 6.1 Commande

```python
@dataclass(frozen=True)
class RefreshSessionCommand:
    refresh_token: str
    ip_address: str | None = None
    user_agent: str | None = None
```

### 6.2 Règles

- vérifier le refresh token via `TokenProvider` ;
- extraire `refresh_token_id` ou `jti` ;
- retrouver la session ;
- refuser session expirée ;
- refuser session révoquée ;
- mettre à jour `last_used_at` ;
- émettre une nouvelle paire de tokens ;
- produire `SESSION_REFRESHED`.

Le refresh token brut ne doit jamais être stocké ni audité.

---

## 7. Cas d'usage `Logout`

### 7.1 Commande

```python
@dataclass(frozen=True)
class LogoutCommand:
    session_id: SessionId
    actor_subject: AuthSubject
```

### 7.2 Règles

- l'utilisateur peut déconnecter sa propre session ;
- l'opération est idempotente ;
- révoquer la session ;
- demander la révocation du token via `TokenProvider` si disponible ;
- produire `LOGOUT`.

---

## 8. Cas d'usage `RevokeSession`

### 8.1 Commande

```python
@dataclass(frozen=True)
class RevokeSessionCommand:
    actor: AuthContext | None
    session_id: SessionId
```

En `0.2.0`, si `AuthContext` n'est pas encore complet, accepter une forme minimale ou reporter les contrôles avancés à `0.3.0`.

### 8.2 Règles

- révoquer une session existante ;
- refuser une session inconnue sauf choix d'idempotence documenté ;
- produire `SESSION_REVOKED` ;
- ne jamais auditer de token brut.

---

## 9. DTO nécessaires

### 9.1 `TokenPair`

```python
@dataclass(frozen=True)
class TokenPair:
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    refresh_expires_in: int
```

`repr()` doit masquer les tokens si possible.

### 9.2 `TokenClaims`

```python
@dataclass(frozen=True)
class TokenClaims:
    subject: AuthSubject
    session_id: SessionId | None
    token_id: TokenId
    roles: tuple[RoleName, ...]
    permissions: tuple[PermissionName, ...]
    issued_at: datetime
    expires_at: datetime
    issuer: str | None
    audience: str | tuple[str, ...] | None
```

### 9.3 `SessionDTO`

Ne contient aucun refresh token brut.

---

## 10. Audit attendu

Événements obligatoires :

```text
USER_REGISTERED
LOGIN_SUCCESS
LOGIN_FAILURE
ACCOUNT_LOCKED
SESSION_REFRESHED
LOGOUT
SESSION_REVOKED
```

Métadonnées interdites :

```text
password
plain_password
password_hash
access_token
refresh_token
private_key
secret
authorization
cookie
```

---

## 11. Tests obligatoires

Créer ou compléter :

```text
tests/application/test_register_user.py
tests/application/test_authenticate_user.py
tests/application/test_refresh_session.py
tests/application/test_logout.py
tests/application/test_revoke_session.py
tests/domain/entities/test_session.py
tests/domain/entities/test_user_login_state.py
tests/security/test_no_secret_leakage.py
```

Cas obligatoires :

- inscription nominale ;
- email déjà utilisé ;
- mot de passe faible ;
- login nominal ;
- email inconnu ;
- mauvais mot de passe ;
- compte verrouillé ;
- verrouillage après N échecs ;
- refresh nominal ;
- refresh session expirée ;
- logout idempotent ;
- révocation session ;
- audit sans secret.

---

## 12. Backlog détaillé

### BL-020-001 — Implémenter `RegisterUser`

### BL-020-002 — Implémenter `AuthenticateUser`

### BL-020-003 — Implémenter lockout minimal

### BL-020-004 — Implémenter `RefreshSession`

### BL-020-005 — Implémenter `Logout`

### BL-020-006 — Implémenter `RevokeSession`

### BL-020-007 — Stabiliser DTO tokens/session

### BL-020-008 — Ajouter audit auth/session

### BL-020-009 — Ajouter tests et documentation

---

## 13. Documentation attendue

Créer ou compléter :

```text
docs/authentication.md
docs/sessions.md
docs/audit.md
docs/security_rules.md
README.md
CHANGELOG.md
```

---

## 14. Critères de définition de terminé

La version `0.2.0` est terminée si :

- `RegisterUser` fonctionne ;
- `AuthenticateUser` fonctionne ;
- `RefreshSession` fonctionne ;
- `Logout` fonctionne ;
- `RevokeSession` fonctionne ;
- le lockout minimal fonctionne ;
- les événements d'audit sont produits ;
- aucun secret n'est exposé ;
- les fakes permettent de tester sans infrastructure ;
- `ruff`, `mypy`, `pytest` passent ;
- couverture ≥ 90 %.
