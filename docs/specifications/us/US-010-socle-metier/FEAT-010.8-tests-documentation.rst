FEAT-010.8 — Ajouter tests et documentation
===========================================

:Rattachée à: :ref:`us-010`
:Issue GitHub: ``[FEAT-010.8]`` (sub-issue de ``[US-010]``)
:Backlog: ``BL-010-008``
:Statut: Implémentée

Description
-----------

Finaliser la qualité : suite de tests unitaires en arborescence miroir,
couverture conforme, et documentation minimale.

Critères d'acceptation
----------------------

#. Tests présents pour chaque value object, entité, policy, fake, et pour la
   hiérarchie d'exceptions.
#. Tests garantissant l'absence de secret dans ``repr()``/``str()``.
#. Test garantissant l'absence de dépendance technique interdite dans le code de
   production.
#. Couverture ≥ 85 % (cible cahier des charges v0.1.0) ; le projet impose en
   interne ≥ 95 % (``--cov-fail-under=95``).
#. ``ruff``, ``mypy`` (strict) et ``pytest`` passent.
#. Documentation minimale disponible : ``README.md``, ``CHANGELOG.md`` et les
   guides ``domain_model``, ``ports``, ``testing``.

Réalisé
-------

234 tests unitaires, couverture **98,89 %**. Guides livrés en RST sous
``docs/guides/``.

Tâches (suivies dans ``docs/backlog/``)
---------------------------------------

* ``TASK-010.8.1`` Écrire les tests miroir manquants.
* ``TASK-010.8.2`` Rédiger les guides ``domain_model``, ``ports``, ``testing``.
* ``TASK-010.8.3`` Vérifier la couverture et les gates qualité.
