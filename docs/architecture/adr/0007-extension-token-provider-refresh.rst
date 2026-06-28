ADR-0007 — Extension du port ``TokenProvider`` (refresh tokens et révocation)
============================================================================

:Statut: Accepté
:Date: 2026-06-28
:Version: v0.2.0
:Backlogs: BL-020-004, BL-020-005

Contexte
--------

Le port ``TokenProvider`` de la v0.1.0 n'expose que la gestion des **tokens
d'accès** (``create_access_token``, ``verify_access_token``,
``generate_token_id``). Les cas d'usage ``AuthenticateUser``, ``RefreshSession``
et ``Logout`` de la v0.2.0 nécessitent d'**émettre** et de **vérifier** un
*refresh token*, et optionnellement de **révoquer** un token.

Décision
--------

Étendre le ``Protocol`` ``TokenProvider`` avec des méthodes additives :

- ``create_refresh_token(subject, token_id, ttl_seconds, claims=None) -> str``
- ``verify_refresh_token(token) -> dict`` — retourne le payload contenant le
  ``refresh_token_id`` / ``jti``.
- ``revoke_token(token) -> None`` — révocation best-effort, optionnelle côté
  implémentation (``Logout`` l'appelle « si disponible »).

Le ``FakeTokenProvider`` est étendu en conséquence pour permettre les tests sans
infrastructure. Le *refresh token brut* n'est jamais stocké ni audité ; seul son
identifiant (``refresh_token_id``) est persisté sur la ``Session``.

Conséquences
------------

- **Évolution de contrat** : ajout de méthodes au port public. Comme la cible
  est pré-1.0 et l'ajout est additif (capacité nouvelle), il est traité comme un
  incrément **MINOR** documenté au CHANGELOG.
- Les implémentations concrètes existantes doivent fournir les nouvelles méthodes.
- Le domaine reste pur : aucune dépendance JWT/PASETO n'est introduite dans le core.
