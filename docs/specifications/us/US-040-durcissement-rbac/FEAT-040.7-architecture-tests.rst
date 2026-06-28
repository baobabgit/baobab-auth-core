FEAT-040.7 — Tests d'architecture anti-dépendances
==================================================

:Rattachée à: :ref:`us-040`
:Statut: Implémentée

Description
-----------

Test garantissant l'absence de dépendance d'infrastructure dans ``src/``.

Critères d'acceptation
----------------------

#. Aucun import interdit (fastapi, sqlalchemy, jwt, argon2, bcrypt, httpx, requests, os.environ, open, socket) dans ``src/``.
