Sessions et tokens (v0.2.0)
===========================

Cycle de vie d'une session
--------------------------

Une :class:`~baobab_auth_core.domain.entities.session.Session` est créée à la
connexion (``ACTIVE``), peut être rafraîchie, puis ``REVOKED`` (logout /
révocation) ou ``EXPIRED`` (TTL dépassé). L'entité porte le comportement métier :
``is_active``, ``is_expired``, ``mark_used``, ``rotate_refresh_token``,
``revoke`` (idempotent) et ``expire``.

Rafraîchissement — ``RefreshSession``
-------------------------------------

.. code-block:: python

   from baobab_auth_core.application.commands.refresh_session_command import (
       RefreshSessionCommand,
   )
   from baobab_auth_core.application.use_cases.refresh_session import RefreshSession

   use_case = RefreshSession(
       sessions, users, audit, token_provider, id_generator, clock, uow,
   )
   result = use_case.execute(RefreshSessionCommand(refresh_token=raw_refresh_token))

Le refresh token est vérifié via le port ``TokenProvider`` ; la session est
retrouvée par son ``refresh_token_id`` (jamais par le token brut), puis le token
est **tourné** (rotation). Une session révoquée ou expirée est refusée
(``SessionRevokedError`` / ``SessionExpiredError``). Audit : ``SESSION_REFRESHED``.

Déconnexion et révocation
-------------------------

- ``Logout`` (``LogoutCommand``) révoque la **propre** session de l'acteur, de
  façon **idempotente** ; audit ``LOGOUT``.
- ``RevokeSession`` (``RevokeSessionCommand``) révoque une session existante ;
  audit ``SESSION_REVOKED``. En v0.2.0 l'acteur est minimal (``AuthSubject``) ;
  les contrôles d'autorisation fins arrivent en v0.3.0 (ADR-0008).

Verrouillage (lockout minimal)
------------------------------

Après ``SessionPolicy.max_failed_login_attempts`` échecs consécutifs, le compte
est verrouillé jusqu'à ``now + lockout_duration_seconds`` et un audit
``ACCOUNT_LOCKED`` est émis. Un succès réinitialise le compteur ; passé le délai,
le compte est automatiquement déverrouillé à la prochaine tentative valide.
