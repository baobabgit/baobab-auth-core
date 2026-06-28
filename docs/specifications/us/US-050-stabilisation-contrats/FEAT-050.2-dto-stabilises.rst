FEAT-050.2 — DTO applicatifs stabilisés
=======================================

:Rattachée à: :ref:`us-050`
:Statut: Implémentée

Description
-----------

``AuthenticatedUser`` (roles + permissions, sans secret), ``SessionDTO``, ``TokenPair``, ``TokenClaims`` et nouveau ``TokenIssueContext``.

Critères d'acceptation
----------------------

#. ``AuthenticatedUser`` expose ``roles`` et ``permissions``, jamais de secret.
#. ``TokenIssueContext`` fournit subject/user_id/session_id/roles/permissions/issued_at/access_expires_at/refresh_expires_at/issuer/audience.
