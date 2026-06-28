FEAT-040.4 — Audit JWK_ROTATION_REQUESTED
=========================================

:Rattachée à: :ref:`us-040`
:Statut: Implémentée

Description
-----------

Événement d'audit ``JWK_ROTATION_REQUESTED`` (CRITICAL) et cas d'usage ``RequestJwkRotation`` réservé ``SUPER_ADMIN``.

Critères d'acceptation
----------------------

#. ``JWK_ROTATION_REQUESTED`` existe et est CRITICAL à l'émission.
#. Seul un acteur ``SUPER_ADMIN`` peut déclencher la demande (``ForbiddenError`` sinon).
