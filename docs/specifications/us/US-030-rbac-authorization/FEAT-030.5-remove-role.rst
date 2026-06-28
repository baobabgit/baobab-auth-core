FEAT-030.5 — Stabiliser RemoveRole
==================================

:Rattachée à: :ref:`us-030`
:Backlog: ``BL-030-005``
:Statut: TODO

Description
-----------

Créer le cas d'usage ``RemoveRole`` pour retirer un rôle d'un utilisateur cible
avec autorisation minimale, idempotence, protection du dernier ``SUPER_ADMIN`` et audit.

Critères d'acceptation
----------------------

#. L'acteur, la cible et le rôle sont validés.
#. L'acteur doit porter ``ADMIN`` ou ``SUPER_ADMIN`` en v0.3.0.
#. Le retrait est idempotent si la cible ne possède pas le rôle.
#. Le dernier ``SUPER_ADMIN`` ne peut pas être retiré.
#. L'audit ``ROLE_REMOVED`` est produit sans secret.
