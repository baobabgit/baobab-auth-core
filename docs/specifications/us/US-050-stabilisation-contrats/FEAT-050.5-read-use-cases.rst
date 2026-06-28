FEAT-050.5 — Cas d'usage de lecture
===================================

:Rattachée à: :ref:`us-050`
:Statut: Implémentée

Description
-----------

``GetUserBySubject``, ``GetCurrentUser``, ``ListRoles``, ``ListPermissions``, ``ListUserSessions``.

Critères d'acceptation
----------------------

#. Chaque lecture a query + résultat ; aucune mutation, aucun secret retourné.
#. ``GetCurrentUser`` agrège rôles et permissions via l'``AuthorizationService``.
