# Rapport d'intégration — baobab-auth-core v0.5.1 × baobab-auth-security v0.1.0

Date : 2026-06-30  
Producteur : baobab-auth-core  
Consommateur : baobab-auth-security (git-ref `version/v0.1.0`)  
Résultat : **PASSED**

## Fonctionnalités core validées par security v0.1.0

| Domaine core | Usage security v0.1.0 |
|---|---|
| `ports.password_hasher.PasswordHasher` | `CorePasswordHasherAdapter` (Argon2id) |
| `ports.token_provider.TokenProvider` | `CoreTokenProviderAdapter` (JWT RS256) |
| `application.results.token_claims.TokenClaims` | `CoreClaimsMapper` |
| `application.results.token_pair.TokenPair` | `CoreTokenPairMapper` |
| `domain.value_objects.token_id.TokenId` | `CoreRevocationAdapter` |
| `domain.value_objects.plain_password.PlainPassword` | Hachage / vérification |
| `domain.value_objects.password_hash.PasswordHash` | Stockage hash typé |
| `exceptions.auth.TokenInvalidError` | Traduction erreurs JWT |
| `exceptions.auth.TokenExpiredError` | Traduction expiration JWT |

## Scénarios d'intégration

- Hachage et vérification via le port `PasswordHasher` (contrat synchrone réel).
- Émission / vérification access et refresh tokens via `TokenProvider`.
- Mapping `SecurityTokenClaims` → `TokenClaims` et paire → `TokenPair`.
- Révocation par `TokenId` via `CoreRevocationAdapter`.
- Tests contractuels : `tests/integration/core/` (169 tests, couverture 100 %).

## Qualité consommateur

- `uv run nox -s all` : **PASSED**.
- Dépendance : `baobab-auth-core>=0.4.0,<1.0.0` (validé contre PyPI `v0.5.1`).

## Référence

Rapport consommateur : `baobab-auth-security` —
`docs/integrations/reports/baobab-auth-core-v0.5.1__baobab-auth-security-v0.1.0.md`
