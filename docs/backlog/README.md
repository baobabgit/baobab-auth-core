# Backlog (suivi opérationnel)

Ce dossier **matérialise** la chaîne de traçabilité opérationnelle dérivée des
spécifications (`docs/specifications/`). Il est la **source durable** du backlog ;
les Issues GitHub en sont un miroir de suivi, pas l'inverse.

## Convention (tranchée)

| Niveau | Dossier | Format | Rôle |
|--------|---------|--------|------|
| User Story | `user_stories/US-XXX.md` | Markdown | Besoin regroupant des features |
| Feature | `features/FEAT-XXX.Y.md` | Markdown | Découpe fonctionnelle d'une US |
| Backlog | `backlogs/BL-XXX-NNN.md` | Markdown | Unité d'implémentation atomique (1 branche `bl/`) |

> **Pourquoi des fichiers et non seulement des Issues GitHub ?**
> `AGENTS.md` (source unique de vérité) prescrit l'arborescence
> `docs/backlog/{user_stories,features,backlogs}`. Les fiches versionnées
> survivent au dépôt, sont diffables et restent cohérentes avec les
> `status.yaml` du workflow. Les Issues GitHub portent la discussion et le
> suivi temps réel ; elles référencent ces fiches par leur identifiant.

## Distinction avec `docs/specifications/`

- **`docs/specifications/us/`** — le *besoin* stable (US → FEAT) en RST, dérivé du
  cahier des charges. Change rarement.
- **`docs/backlog/`** — le *plan d'exécution* (BL, TASK, statut, dépendances,
  priorité). Vit au rythme du développement.

## Chaîne d'identifiants

```
US-010  →  FEAT-010.1 … FEAT-010.8  →  BL-010-001 … BL-010-008  →  TASK-010.Y.Z
```

L'état machine de chaque backlog est porté par
`docs/ai_workflow/state/queue.yaml` et `docs/ai_workflow/state/dependency_graph.yaml`.
