ADR-0003 — Ports en ``typing.Protocol`` runtime_checkable
=========================================================

:Statut: Accepté
:Date: 2026-06-26
:Contexte version: v0.1.0
:Spec: FEAT-010.6

Contexte
--------

Les ports définissent les frontières que le domaine attend de l'extérieur
(``UserRepository``, ``PasswordHasher``, ``Clock``…). Les projets parents
fournissent leurs propres adapters. Il faut un mécanisme d'interface qui
n'impose **aucun héritage** aux implémentations tierces.

Décision
--------

Définir chaque port comme un ``typing.Protocol`` décoré ``@runtime_checkable`` :

.. code-block:: python

    @runtime_checkable
    class Clock(Protocol):
        def now(self) -> datetime: ...

Les implémentations (réelles ou fakes) **n'héritent pas** du protocole : la
conformité est structurelle (duck typing). ``@runtime_checkable`` permet en outre
``isinstance(impl, Clock)`` dans les tests de contrat.

Conséquences
------------

**Positives**

* Découplage total : un adapter parent ne dépend pas d'une classe de base du core.
* Vérification structurelle par ``mypy`` à la compilation, et par ``isinstance``
  au runtime pour les tests.
* Signatures homogènes (toutes synchrones en v0.1.0), documentées en RST.

**Négatives / coûts**

* ``@runtime_checkable`` ne vérifie que la présence des méthodes, pas leurs
  signatures à l'exécution → la garantie fine repose sur ``mypy``.
* Les protocoles ne peuvent pas fournir d'implémentation par défaut partagée.

Alternatives écartées
---------------------

* **Classes Abstraites (``abc.ABC``)** : rejetées car elles imposeraient un
  héritage explicite aux adapters des projets parents, recréant un couplage.
* **Interfaces implicites non typées** : rejetées (perte du typage strict
  ``mypy``).
