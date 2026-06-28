FEAT-050.4 — Contrats database et security
==========================================

:Rattachée à: :ref:`us-050`
:Statut: Implémentée

Description
-----------

Ports repositories, ``PasswordHasher`` et ``TokenProvider`` stabilisés ; ``DefaultAuthCatalog`` utilisable pour le seed.

Critères d'acceptation
----------------------

#. Aucune connaissance des noms de tables dans le core ; ``AuditEvent.metadata`` JSON-sérialisable ; dates UTC aware.
#. ``sub``=AuthSubject, ``jti``=TokenId, ``sid``=SessionId ; pas de JWT/Argon2 concret.
