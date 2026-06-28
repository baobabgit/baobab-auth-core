FEAT-050.1 — Exports publics stabilisés
=======================================

:Rattachée à: :ref:`us-050`
:Statut: Implémentée

Description
-----------

API publique exhaustive dans ``baobab_auth_core.__all__`` + tests d'import.

Critères d'acceptation
----------------------

#. Entités, value objects, enums, policies, catalogues, ports, DTO et use cases exportés.
#. Tests d'import vérifiant que chaque symbole de ``__all__`` est importable.
