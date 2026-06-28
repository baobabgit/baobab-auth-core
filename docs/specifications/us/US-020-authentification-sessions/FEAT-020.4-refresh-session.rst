FEAT-020.4 — Implémenter RefreshSession
=======================================

:Rattachée à: :ref:`us-020`
:Backlog: ``BL-020-004``
:Statut: Implémentée

Description
-----------

Cas d'usage `RefreshSession` + extension refresh du port `TokenProvider`.

Critères d'acceptation
----------------------

#. Vérifie le refresh token via `TokenProvider`, extrait `refresh_token_id`/`jti`.
#. Refuse session expirée/révoquée, met à jour `last_used_at`.
#. Émet une nouvelle `TokenPair`, produit `SESSION_REFRESHED`.
#. Ne stocke ni n'audite jamais le refresh token brut.
