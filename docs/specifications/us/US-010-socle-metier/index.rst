.. _us-010:

US-010 — Disposer d'un socle métier d'authentification réutilisable
===================================================================

:Statut: Implémentée (v0.1.0)
:Issue GitHub: ``[US-010]`` (à créer)
:Origine: cahier des charges ``baobab-auth-core`` v0.1.0
:Version cible: v0.1.0

Récit
-----

**En tant qu'**\ équipe intégrant ``baobab-auth-core`` dans un projet parent,
**je veux** un socle métier d'authentification pur (entités, value objects,
policies, exceptions, ports et fakes),
**afin de** construire les parcours d'authentification des versions suivantes
sans jamais réécrire le domaine ni dépendre d'une brique technique.

Contexte
--------

La version ``0.1.0`` pose le **socle métier minimal**. Elle fournit les objets du
domaine, les value objects, les policies de base, les exceptions, les ports
principaux et les fakes nécessaires aux tests. Elle ne fournit **pas** encore un
parcours complet d'authentification avec sessions et tokens (couche
``application`` reportée à une version ultérieure).

Contrainte d'architecture constante : le core reste une **librairie métier pure**,
sans FastAPI, SQLAlchemy, Alembic, PostgreSQL, JWT concret, Argon2, bcrypt, httpx,
requests, Docker, ni accès fichier/réseau/variable d'environnement en production.

Critères d'acceptation
----------------------

#. Le package ``baobab_auth_core`` s'installe et le domaine est importable.
#. Les entités principales existent (``User``, ``UserProfile``, ``Role``,
   ``Permission``, ``Session``, ``AuditEvent``).
#. Les value objects principaux existent et appliquent leurs règles de
   normalisation/validation.
#. Les policies existent (``PasswordPolicy``, ``SessionPolicy``, ``RolePolicy``).
#. La hiérarchie d'exceptions métier existe.
#. Les ports (protocoles) existent et sont homogènes.
#. Les fakes in-memory existent pour tous les ports.
#. Aucun import technique interdit n'est présent dans le code de production.
#. ``ruff``, ``mypy`` et ``pytest`` passent ; couverture ≥ 85 % (cible interne
   du projet : ≥ 95 %).
#. La documentation minimale est disponible.

Découpage en Features
---------------------

L'US est découpée en huit features, chacune rattachée à un backlog atomique
(``BL-010-00X``) suivi dans :doc:`/specifications/index`.

================  ==========================================  =============
Feature           Intitulé                                    Backlog
================  ==========================================  =============
``FEAT-010.1``    Initialiser le package                      ``BL-010-001``
``FEAT-010.2``    Implémenter les value objects               ``BL-010-002``
``FEAT-010.3``    Implémenter les entités                     ``BL-010-003``
``FEAT-010.4``    Implémenter enums et policies               ``BL-010-004``
``FEAT-010.5``    Implémenter les exceptions                  ``BL-010-005``
``FEAT-010.6``    Définir les ports                           ``BL-010-006``
``FEAT-010.7``    Implémenter les fakes in-memory             ``BL-010-007``
``FEAT-010.8``    Ajouter tests et documentation              ``BL-010-008``
================  ==========================================  =============

.. toctree::
   :maxdepth: 1
   :caption: Features

   FEAT-010.1-initialiser-package
   FEAT-010.2-value-objects
   FEAT-010.3-entites
   FEAT-010.4-enums-policies
   FEAT-010.5-exceptions
   FEAT-010.6-ports
   FEAT-010.7-fakes
   FEAT-010.8-tests-documentation
