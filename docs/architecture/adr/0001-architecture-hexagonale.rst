ADR-0001 — Architecture hexagonale (domain / ports / testing)
=============================================================

:Statut: Accepté
:Date: 2026-06-26
:Contexte version: v0.1.0
:Spec: US-010

Contexte
--------

``baobab-auth-core`` est une **librairie consommable** destinée à être intégrée
dans des projets parents hétérogènes (web, CLI, workers). Le cahier des charges
v0.1.0 impose un cœur métier réutilisable sans réécriture lors des versions
suivantes, et interdit toute dépendance technique en production.

Décision
--------

Adopter une **architecture hexagonale** (ports & adapters) avec la séparation
suivante dans ``src/baobab_auth_core/`` :

* ``domain/`` — entités, value objects, enums, policies, services. Ne dépend de
  rien d'externe.
* ``ports/`` — interfaces (protocoles) que le domaine requiert de l'extérieur
  (persistance, horloge, hachage, tokens).
* ``exceptions/`` — hiérarchie d'erreurs métier.
* ``testing/`` — implémentations de test (fakes/in-memory) des ports.

La couche ``application/`` (use cases) est **prévue mais reportée** : elle n'est
pas livrée en v0.1.0, qui se limite au socle.

Règles de dépendance :

* le domaine ne dépend pas de ``application`` ;
* les ports ne dépendent d'aucune implémentation ;
* aucun code de production ne dépend d'une brique technique.

Conséquences
------------

**Positives**

* Le domaine est testable sans infrastructure.
* Les projets parents fournissent leurs adapters concrets sans modifier le core.
* L'évolution vers ``application/`` se fait par ajout, sans rupture.

**Négatives / coûts**

* Plus de fichiers et d'indirection qu'une approche en couches simple.
* Nécessite de la discipline pour ne pas « court-circuiter » les ports.

Alternatives écartées
---------------------

* **Architecture en couches classique** (services dépendant directement d'ORM) :
  rejetée car elle couplerait le domaine à une brique technique.
* **Tout dans un seul module** : rejetée (viole 1 classe = 1 fichier et SOLID).
