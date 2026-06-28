FEAT-020.6 — Implémenter RevokeSession
======================================

:Rattachée à: :ref:`us-020`
:Backlog: ``BL-020-006``
:Statut: Implémentée

Description
-----------

Cas d'usage `RevokeSession` (acteur minimal en 0.2.0).

Critères d'acceptation
----------------------

#. Révoque une session existante, idempotence documentée.
#. Produit `SESSION_REVOKED`, n'audite jamais de token brut.
#. `AuthContext` complet reporté à 0.3.0 (acteur minimal).
