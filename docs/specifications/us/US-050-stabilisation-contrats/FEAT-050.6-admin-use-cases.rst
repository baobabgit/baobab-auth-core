FEAT-050.6 — Cas d'usage admin métier
=====================================

:Rattachée à: :ref:`us-050`
:Statut: Implémentée

Description
-----------

``DisableUser``, ``EnableUser``, ``BootstrapSuperAdmin``, ``RequestJwkRotation``.

Critères d'acceptation
----------------------

#. ``DisableUser``/``EnableUser`` audités (``ACCOUNT_DISABLED``/``ACCOUNT_ENABLED``), réservés ADMIN/SUPER_ADMIN.
#. ``BootstrapSuperAdmin`` n'opère que s'il n'existe aucun SUPER_ADMIN (bootstrap système).
