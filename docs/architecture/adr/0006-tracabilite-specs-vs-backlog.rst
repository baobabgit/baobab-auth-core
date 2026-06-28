ADR-0006 — Traçabilité : spécifications stables (RST) vs backlog opérationnel (Markdown)
========================================================================================

:Statut: Accepté
:Date: 2026-06-27
:Contexte version: v0.1.0
:Spec: US-010

Contexte
--------

Le squelette du projet exposait une ambiguïté : ``docs/specifications/index.rst``
affirmait que « le backlog vit dans GitHub Issues / Projects et n'est pas
dupliqué », alors que ``AGENTS.md`` (source unique de vérité) prescrit une
arborescence ``docs/backlog/{user_stories,features,backlogs}``. Résultat : le
dossier ``docs/backlog/`` restait vide et la frontière avec ``docs/specifications/``
n'était pas claire.

Décision
--------

Trancher en faveur de **deux artefacts complémentaires, aux rôles distincts** :

* ``docs/specifications/`` — le **besoin stable**, en **reStructuredText**, intégré
  à Sphinx. Contient le cahier des charges brut déposé et les US/FEAT dérivées.
  Change rarement (au rythme du besoin).
* ``docs/backlog/`` — le **plan d'exécution opérationnel**, en **Markdown**.
  Contient les fiches ``US`` (regroupement), ``FEAT`` (découpe) et surtout les
  fiches ``BL`` (unités d'implémentation : statut, priorité, dépendances,
  Definition of Done). Vit au rythme du développement.

Les **fiches versionnées sont la source durable** ; les Issues GitHub en sont un
**miroir de suivi** (discussion, état temps réel), référençant les identifiants
``US-XXX`` / ``FEAT-XXX.Y`` / ``BL-XXX-NNN`` / ``TASK-XXX.Y.Z``.

L'état machine (sélection du prochain backlog, dépendances) reste porté par
``docs/ai_workflow/state/queue.yaml`` et ``dependency_graph.yaml``.

Conséquences
------------

**Positives**

* Frontière nette : *quoi* (specs RST) vs *comment/quand* (backlog Markdown).
* Traçabilité besoin → code → test reconstituable hors GitHub (diffable, archivée).
* Cohérence avec ``AGENTS.md`` rétablie.

**Négatives / coûts**

* Double tenue possible (fiche + Issue) ; mitigée en traitant l'Issue comme simple
  miroir non normatif.
* Discipline requise pour garder ``queue.yaml`` et les fiches ``BL`` synchronisés.

Alternatives écartées
---------------------

* **Backlog uniquement dans GitHub Issues** : rejetée — non versionné dans le
  dépôt, contraire à ``AGENTS.md``, perdu si le dépôt migre.
* **Tout fusionner dans ``specifications/``** : rejetée — mélange le besoin stable
  et le suivi volatile, brouille la source de vérité.
