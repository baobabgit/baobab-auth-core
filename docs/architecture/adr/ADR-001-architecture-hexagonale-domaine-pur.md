# ADR-001 — Architecture hexagonale et domaine pur

- **Statut** : Accepté
- **Date** : 2026-06-26
- **Version** : v0.1.0
- **Backlogs concernés** : BL-010-001 → BL-010-008

## Contexte

`baobab-auth-core` est une **librairie consommable** destinée à être intégrée
dans des projets parents hétérogènes (API web, workers, CLI). Elle doit exposer
un socle métier d'authentification et d'autorisation stable sans imposer de choix
techniques (ORM, framework web, algorithme de hachage, format de token) à ses
consommateurs.

## Décision

Adopter une **architecture hexagonale (ports & adapters)** avec un **domaine pur**,
sans aucune dépendance de production :

- Le **domaine** (`domain/`) contient les value objects, entités, enums et policies.
  Il est auto-validant et ne dépend d'aucune technologie concrète.
- Les **ports** (`ports/`) déclarent les interfaces attendues
  (repositories, `Clock`, `IdGenerator`, `PasswordHasher`, `TokenProvider`,
  `UnitOfWork`). Les implémentations concrètes restent à la charge du projet parent.
- Des **fakes in-memory** (`testing/`) sont livrés dans le package pour permettre
  aux consommateurs de tester sans infrastructure réelle.
- La configuration éventuelle est **injectée** (`pydantic-settings`) ; aucun état
  global, aucune hypothèse sur l'hôte.

## Conséquences

**Positives**

- Découplage total du métier vis-à-vis de l'infrastructure ; testabilité maximale
  (couverture v0.1.0 : 98.89 %).
- Le contrat public (`__all__`) est stable et versionné en SemVer ; toute rupture
  impose un bump majeur.
- Pas de dépendance de production → empreinte minimale chez le consommateur.

**Négatives / coûts**

- Le projet parent doit fournir les adaptateurs concrets des ports.
- L'ajout d'un nouveau port est une évolution de contrat à tracer (CHANGELOG +
  matrice de compatibilité).

## Alternatives écartées

- **Couplage direct à un ORM / framework** : rejeté car il contraindrait les
  projets parents et romprait la réutilisabilité.
- **Hachage / JWT embarqués** : rejeté pour ne pas figer d'algorithme ni de
  dépendance lourde dans un socle métier.
