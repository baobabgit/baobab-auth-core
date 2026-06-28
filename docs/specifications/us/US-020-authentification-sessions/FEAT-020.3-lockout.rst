FEAT-020.3 — Implémenter le lockout minimal
===========================================

:Rattachée à: :ref:`us-020`
:Backlog: ``BL-020-003``
:Statut: Implémentée

Description
-----------

Verrouillage du compte après N échecs consécutifs.

Critères d'acceptation
----------------------

#. Incrémente `failed_login_count` à chaque échec.
#. Verrouille après `max_failed_login_attempts` et produit `ACCOUNT_LOCKED`.
#. Réinitialise le compteur en cas de succès.
