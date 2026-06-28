FEAT-050.7 — Tests contractuels inter-briques
=============================================

:Rattachée à: :ref:`us-050`
:Statut: Implémentée

Description
-----------

``tests/contracts/{database,security,api,client,admin}/`` validant les contrats publics sans importer d'autre brique.

Critères d'acceptation
----------------------

#. Les tests de contrat n'importent que ``baobab_auth_core`` (jamais database/security/api/client/admin).
