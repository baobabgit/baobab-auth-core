Règles de sécurité (v0.2.0)
===========================

Principes
---------

#. **Aucun secret en clair persisté ou journalisé.** Les mots de passe ne sont
   manipulés que via ``PlainPassword`` (masqué dans ``repr``/``str``) puis hachés
   par le port ``PasswordHasher``. Seul le ``PasswordHash`` est stocké.
#. **Tokens masqués.** ``TokenPair`` masque ``access_token`` et ``refresh_token``
   dans son ``repr``. ``SessionDTO`` n'expose jamais le ``refresh_token_id``.
#. **Refresh token brut jamais stocké ni audité.** La session est retrouvée par
   son ``refresh_token_id`` ; le token brut ne quitte pas la frontière du port
   ``TokenProvider``.
#. **Audit sans secret.** ``AuditMetadataGuard`` rejette toute métadonnée
   sensible (voir :doc:`audit`).
#. **Messages d'échec génériques.** ``AuthenticateUser`` lève
   ``InvalidCredentialsError`` sans divulguer si l'email existe.

Métadonnées d'audit interdites
------------------------------

Toute clé contenant l'un de ces termes est rejetée :

.. code-block:: text

   password   token   secret   hash   authorization   cookie   private_key

Pureté du core
--------------

Le core ne réalise **aucun** hachage cryptographique réel ni génération de JWT :
il orchestre les ports ``PasswordHasher`` et ``TokenProvider``. Aucune dépendance
technique (FastAPI, SQLAlchemy, JWT, Argon2, bcrypt, httpx, Docker) n'est
introduite.
