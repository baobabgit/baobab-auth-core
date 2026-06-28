FEAT-050.3 — Codes d'erreurs métier
===================================

:Rattachée à: :ref:`us-050`
:Statut: Implémentée

Description
-----------

Chaque exception publique expose ``error_code``, ``safe_message`` et un ``http_status`` recommandé.

Critères d'acceptation
----------------------

#. ``InvalidCredentialsError`` → ``auth.credentials.invalid`` (401), ``ForbiddenError`` → ``auth.authorization.forbidden`` (403), etc.
#. ``safe_message`` ne divulgue aucun détail sensible.
