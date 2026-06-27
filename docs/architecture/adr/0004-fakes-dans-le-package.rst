ADR-0004 — Fakes livrés dans le package (``testing/``)
======================================================

:Statut: Accepté
:Date: 2026-06-26
:Contexte version: v0.1.0
:Spec: FEAT-010.7

Contexte
--------

Les ports sont abstraits ; tester du code qui les consomme exige des
implémentations légères et déterministes (horloge contrôlable, repositories en
mémoire, hasher simulé). La question est de savoir **où** vivent ces fakes : dans
les tests internes (``tests/``) ou dans le package distribué.

Décision
--------

Livrer les fakes dans un sous-package public ``baobab_auth_core.testing`` :

* ``FakeClock``, ``FakeIdGenerator``, ``FakePasswordHasher``, ``FakeTokenProvider`` ;
* ``InMemory{User,Role,Permission,Session,Audit}Repository`` ;
* ``InMemoryUnitOfWork``.

Ces fakes font **partie du contrat** : un projet parent les importe pour tester
son intégration au domaine sans réécrire des doublures.

Conséquences
------------

**Positives**

* Les consommateurs testent leur intégration avec des doublures officielles et
  maintenues.
* Les fakes sont eux-mêmes couverts par des tests → fiables.
* Évite la duplication de doublures dans chaque projet parent.

**Négatives / coûts**

* Les fakes sont du code livré : ils entrent dans le contrat SemVer (une rupture
  de leur API publique impose un bump majeur).
* Légère augmentation de la surface du package.

Alternatives écartées
---------------------

* **Fakes confinés dans ``tests/``** : rejetée car non réutilisables par les
  consommateurs.
* **Package séparé ``baobab-auth-core-testing``** : rejetée pour v0.1.0
  (surcoût de publication non justifié ; pourra être reconsidéré ultérieurement).
