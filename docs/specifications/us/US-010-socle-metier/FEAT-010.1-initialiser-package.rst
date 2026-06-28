FEAT-010.1 — Initialiser le package
===================================

:Rattachée à: :ref:`us-010`
:Issue GitHub: ``[FEAT-010.1]`` (sub-issue de ``[US-010]``)
:Backlog: ``BL-010-001``
:Statut: Implémentée

Description
-----------

Mettre en place le squelette de la librairie : structure ``src/`` en layout
hexagonal, métadonnées du package, marqueur de typage et fichiers projet de base.

Critères d'acceptation
----------------------

#. ``pyproject.toml`` déclare le package ``baobab-auth-core`` (nom de
   distribution) et le module importable ``baobab_auth_core``.
#. Le fichier ``src/baobab_auth_core/py.typed`` est présent (PEP 561).
#. Les sous-packages ``domain/`` (``entities/``, ``value_objects/``, ``enums/``,
   ``policies/``, ``services/``), ``ports/``, ``exceptions/`` et ``testing/`` sont
   créés.
#. ``README.md`` et ``CHANGELOG.md`` existent.
#. ``import baobab_auth_core`` réussit dans un environnement fraîchement installé.

Règles d'architecture appliquées
--------------------------------

* le domaine ne dépend pas de la couche ``application`` ;
* les ports ne dépendent d'aucune implémentation ;
* aucun code de production ne dépend d'une brique technique.

Tâches (suivies dans ``docs/backlog/``)
---------------------------------------

* ``TASK-010.1.1`` Créer le layout ``src/`` et les ``__init__.py``.
* ``TASK-010.1.2`` Configurer ``pyproject.toml`` (build, outils qualité).
* ``TASK-010.1.3`` Ajouter ``py.typed``, ``README.md``, ``CHANGELOG.md``.
