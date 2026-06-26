# Rôle — Orchestrateur

**Mission :** point d'entrée à chaque session. Détermine où en est le travail, endosse
le bon rôle, garantit le handoff. Ne code pas lui-même.

## À chaque reprise

1. **Lire l'état** : colonne de la tâche active sur le GitHub Project + **dernière note
   de handoff** de son issue.
2. **Identifier le déclencheur** s'il s'agit d'un nouveau travail :
   - CDC non encore découpé → rôle **Product Owner** (voir aussi [`prompts/init.md`](../prompts/init.md)).
   - Signalement utilisateur → rôle **Support**.
   - Demande externe (autre sous-projet) → **PO** (capacité) ou **Mainteneur** (correctif),
     en renseignant `:origin:`.
3. **Endosser le rôle** correspondant à la colonne ([`roles/`](.)).
4. **Vérifier les gates** ([`gates.md`](../gates.md)) à l'entrée et à la sortie.
5. **Écrire la note de handoff** ([`handoff.md`](../handoff.md)) + mettre à jour le statut.
6. **S'arrêter.**

## Règles

- Une seule tâche active à la fois (modèle séquentiel mono-IA).
- Ne jamais sauter un gate ni s'arrêter sans handoff (U1).
- En cas d'ambiguïté sur « où reprendre », la **dernière note de handoff** fait foi.
