Audit (v0.2.0)
==============

Les cas d'usage produisent des événements d'audit immuables
(:class:`~baobab_auth_core.domain.entities.audit_event.AuditEvent`) via le
service ``AuditRecorder`` et le port ``AuditRepository``.

Événements émis
---------------

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Événement
     - Sévérité
     - Déclencheur
   * - ``USER_REGISTERED``
     - INFO
     - Inscription réussie
   * - ``LOGIN_SUCCESS``
     - INFO
     - Authentification réussie
   * - ``LOGIN_FAILURE``
     - WARNING
     - Email inconnu, mauvais mot de passe, compte refusé
   * - ``ACCOUNT_LOCKED``
     - WARNING
     - Seuil d'échecs atteint
   * - ``SESSION_REFRESHED``
     - INFO
     - Rafraîchissement de session
   * - ``LOGOUT``
     - INFO
     - Déconnexion
   * - ``SESSION_REVOKED``
     - WARNING
     - Révocation de session

Garde anti-fuite
----------------

``AuditMetadataGuard`` rejette (``ValidationError``) toute métadonnée dont la clé
contient un terme sensible : ``password``, ``token``, ``secret``, ``hash``,
``authorization``, ``cookie``, ``private_key``. Aucun mot de passe, hash ou token
brut ne doit donc jamais apparaître dans l'audit (voir :doc:`security_rules`).
