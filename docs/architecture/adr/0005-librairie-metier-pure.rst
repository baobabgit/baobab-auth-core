ADR-0005 — Librairie métier pure, sans dépendance technique en production
=========================================================================

:Statut: Accepté
:Date: 2026-06-26
:Contexte version: v0.1.0
:Spec: US-010

Contexte
--------

Le cahier des charges pose une **règle d'architecture constante** : le core reste
une librairie métier pure, sans FastAPI, SQLAlchemy, Alembic, PostgreSQL, JWT
concret, Argon2, bcrypt, httpx, requests, Docker, ni accès fichier/réseau/variable
d'environnement en production. L'objectif est la réutilisabilité maximale et
l'absence d'hypothèse sur l'hôte.

Décision
--------

* **Zéro dépendance de production** : le package ne déclare aucune dépendance
  d'exécution. Les briques techniques (hachage réel, JWT, ORM…) sont fournies par
  les projets parents via les ports.
* La cryptographie, la persistance et le temps réel sont **abstraits par des
  ports** ; le core n'en fournit que des fakes (testing).
* Un **test de garde** vérifie l'absence d'import technique interdit dans le code
  de production.
* La configuration éventuelle passe par injection (``pydantic-settings`` côté
  hôte), jamais par lecture d'environnement dans le core.

Conséquences
------------

**Positives**

* Installation triviale, surface d'attaque minimale, aucune contrainte de version
  d'ORM/framework imposée aux consommateurs.
* Le domaine reste stable même si l'écosystème technique évolue.

**Négatives / coûts**

* Les fonctionnalités « concrètes » (vrai hachage, vrais tokens) doivent être
  fournies par l'hôte → plus de travail d'intégration côté consommateur.
* Nécessite un garde-fou automatisé (test) pour empêcher les régressions.

Alternatives écartées
---------------------

* **Inclure un hasher/JWT par défaut (bcrypt, PyJWT)** : rejetée car elle
  imposerait des dépendances et des choix techniques aux consommateurs.
* **Lecture directe d'``os.environ`` dans le core** : rejetée (état global,
  hypothèse sur l'hôte).
