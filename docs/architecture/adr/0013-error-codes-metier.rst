ADR-0013 — Codes d'erreur métier sur les exceptions publiques
============================================================

:Statut: Accepté
:Date: 2026-06-28
:Version: v0.5.0
:Backlogs: BL-050-003

Contexte
--------

Les briques consommatrices (``api``, ``client``) ont besoin de traduire les
exceptions du core en réponses stables (code d'erreur applicatif, message sûr,
statut HTTP) **sans** que le core ne dépende d'un framework web ni ne lève de
``HTTPException``.

Décision
--------

Doter ``BaobabAuthCoreError`` et chaque exception publique de trois attributs de
classe :

- ``error_code: str`` — code stable et hiérarchique (ex. ``auth.user.not_found``) ;
- ``safe_message: str`` — message générique sans détail sensible, retournable au
  client ;
- ``http_status: int`` — statut HTTP **recommandé** (simple entier, jamais une
  ``HTTPException``).

Le message détaillé reste accessible via ``str(exc)`` / ``exc.message`` pour les
logs internes ; ``safe_message`` est la version publique.

Conséquences
------------

- Contrat d'erreur stable et versionné, consommable par ``api``/``client``.
- Le core ne gagne aucune dépendance web : ``http_status`` n'est qu'une
  recommandation.
- Tout nouveau code d'erreur public doit définir ces trois attributs (testé).
