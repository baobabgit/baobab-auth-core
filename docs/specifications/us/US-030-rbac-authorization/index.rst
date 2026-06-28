.. _us-030:

US-030 — RBAC et autorisation métier
====================================

:Version cible: v0.3.0
:Origine: Cahier des charges ``baobab-auth-core`` v0.3.0
:Statut: Ready

Récit
-----

En tant qu'équipe intégrant ``baobab-auth-core``, je veux construire un contexte
d'autorisation et gérer les rôles et permissions côté métier, afin de décider si
un utilisateur peut exécuter une action sans dépendre d'une API HTTP, d'une base
de données ou d'un fournisseur de tokens concret.

Features
--------

.. toctree::
   :maxdepth: 1

   FEAT-030.1-auth-context
   FEAT-030.2-authorization-service
   FEAT-030.3-ports-policies-fakes
   FEAT-030.4-assign-role
   FEAT-030.5-remove-role
   FEAT-030.6-rbac-exceptions
   FEAT-030.7-rbac-audit-tests
   FEAT-030.8-rbac-documentation
