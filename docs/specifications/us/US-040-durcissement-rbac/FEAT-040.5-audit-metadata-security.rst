FEAT-040.5 — Sécurisation des metadata d'audit
==============================================

:Rattachée à: :ref:`us-040`
:Statut: Implémentée

Description
-----------

Garde anti-fuite : aucune clé sensible dans les métadonnées d'audit.

Critères d'acceptation
----------------------

#. ``password``, ``*_token``, ``secret``, ``*_hash``, ``authorization``, ``cookie``, ``private_key`` rejetés.
