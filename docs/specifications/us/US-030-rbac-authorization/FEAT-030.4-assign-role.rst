FEAT-030.4 — Stabiliser AssignRole
==================================

:Rattachée à: :ref:`us-030`
:Backlog: ``BL-030-004``
:Statut: TODO

Description
-----------

Créer le cas d'usage ``AssignRole`` pour affecter un rôle existant à un utilisateur
cible avec autorisation minimale, idempotence et audit.

Critères d'acceptation
----------------------

#. L'acteur, la cible et le rôle sont validés.
#. L'acteur doit porter ``ADMIN`` ou ``SUPER_ADMIN`` en v0.3.0.
#. L'assignation est idempotente si la cible possède déjà le rôle.
#. L'audit ``ROLE_ASSIGNED`` est produit sans secret.
#. La transaction est atomique.
