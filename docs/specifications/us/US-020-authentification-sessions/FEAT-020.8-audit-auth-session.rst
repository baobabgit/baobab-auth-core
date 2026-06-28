FEAT-020.8 — Ajouter l'audit auth/session
=========================================

:Rattachée à: :ref:`us-020`
:Backlog: ``BL-020-008``
:Statut: Implémentée

Description
-----------

Production et garde des événements d'audit auth/session.

Critères d'acceptation
----------------------

#. Émet les 7 événements obligatoires (USER_REGISTERED … SESSION_REVOKED).
#. Refuse les métadonnées sensibles (`password`, `*_token`, `secret`, …).
#. Aucun secret n'apparaît dans l'audit.
