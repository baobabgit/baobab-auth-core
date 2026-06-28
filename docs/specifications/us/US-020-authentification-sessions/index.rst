.. _us-020:

US-020 — Authentification et gestion de session
===============================================

:Version cible: v0.2.0
:Origine: Cahier des charges ``baobab-auth-core`` v0.2.0
:Statut: Implémentée

Récit
-----

En tant qu'équipe intégrant ``baobab-auth-core``, je veux des cas d'usage
d'authentification et de gestion de session orchestrant les ports
``PasswordHasher`` et ``TokenProvider``.

Features
--------

.. toctree::
   :maxdepth: 1

   FEAT-020.1-register-user
   FEAT-020.2-authenticate-user
   FEAT-020.3-lockout
   FEAT-020.4-refresh-session
   FEAT-020.5-logout
   FEAT-020.6-revoke-session
   FEAT-020.7-dto-tokens-session
   FEAT-020.8-audit-auth-session
