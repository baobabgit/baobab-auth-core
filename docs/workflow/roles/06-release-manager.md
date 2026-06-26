# Rôle — Release Manager / DevOps

**Mission :** intégrer, versionner, publier. Assure aussi la **maintenance légère**
(Dependabot, santé CI) tant que le rôle Mainteneur n'est pas détaché.
**Boucle :** construction · **Colonne :** Done

## Definition of Ready
- Review passée (+ Sécurité si déclenchée), CI verte.

## Actions
- **Fusionner** la PR (`Closes #`).
- Si release :
  - mettre à jour `CHANGELOG.md` (section « BREAKING » si rupture d'API publique) ;
  - créer le **tag** `vX.Y.Z` (rupture d'API publique → **majeur**). Le tag *est* la
    version (`hatch-vcs`) — **ne pas** éditer de numéro dans `pyproject.toml`.
  - Le tag déclenche `release.yml` : build (avec attestation de provenance) →
    **PyPI public** (OIDC) + **Release GitHub** avec `sdist`/`wheel` + SBOM attachés.
  - Pour répéter sans risque : tag de **pré-release** (`vX.Y.Zrc1`) → publie sur
    **TestPyPI** au lieu de PyPI.
- Vérifier la santé de la CI / les PR Dependabot en attente.

## Definition of Done (+ U1, U2)
- PR mergée, issue close ; si release : version bumpée, CHANGELOG à jour, tag créé.

## Handoff
- `status: Security|In review -> Done`, `Prochaine action : aucune (tâche close)`.
- Rôle suivant : **Orchestrateur** (tâche suivante).
