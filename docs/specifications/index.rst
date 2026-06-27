Spécifications (cahier des charges)
===================================

Cette section est la **source de vérité stable** du besoin. Elle décrit les
**User Stories (US)** et leurs **Features (FEAT)**. Le **backlog** (les fiches
``BL`` et tâches ``TASK``, opérationnelles) est matérialisé dans
``docs/backlog/`` ; les Issues GitHub en sont le miroir de suivi, pas la source.

Le **cahier des charges brut** (entrée humaine) se dépose dans
``cahier-des-charges/`` ; le rôle Product Owner en dérive les ``us/`` ci-dessous.
Chaque US/FEAT porte un champ ``:Origine:`` indiquant sa provenance (cahier des
charges ou projet externe demandeur).

Hiérarchie et identifiants
--------------------------

================  =====================  ==============================
Niveau            Identifiant            Suivi
================  =====================  ==============================
User Story        ``US-010``             Issue GitHub ``[US-010]``
Feature           ``FEAT-010.1``         Sub-issue ``[FEAT-010.1]``
Backlog           ``BL-010-001``         ``docs/backlog/backlogs/``
Tâche             ``TASK-010.1.1``       Sub-issue ``[TASK-010.1.1]``
================  =====================  ==============================

Ces identifiants sont propagés dans les commits, les noms de tests et les
docstrings (champ ``:spec:``), assurant la traçabilité besoin → code → test.

.. toctree::
   :maxdepth: 2
   :caption: User Stories

   us/index

.. toctree::
   :maxdepth: 1

   glossary
