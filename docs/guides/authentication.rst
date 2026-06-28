Authentification (v0.2.0)
=========================

Cette page décrit les cas d'usage d'authentification de la couche
``application`` et la façon de les câbler avec des adaptateurs concrets ou les
fakes fournis dans ``baobab_auth_core.testing``.

Inscription — ``RegisterUser``
------------------------------

.. code-block:: python

   from baobab_auth_core.application.commands.register_user_command import (
       RegisterUserCommand,
   )
   from baobab_auth_core.application.use_cases.register_user import RegisterUser

   use_case = RegisterUser(users, audit, password_hasher, id_generator, clock, uow)
   result = use_case.execute(
       RegisterUserCommand(email="alice@example.com", password="Sup3rSecret!!")
   )
   # result.user : AuthenticatedUser (sans secret)

Règles appliquées : normalisation de l'email, refus d'un email déjà existant
(``UserAlreadyExistsError``), validation du mot de passe via ``PasswordPolicy``
(``WeakPasswordError``), hachage via le port ``PasswordHasher``, attribution du
rôle ``USER`` et audit ``USER_REGISTERED``, le tout dans une transaction atomique.

Connexion — ``AuthenticateUser``
--------------------------------

.. code-block:: python

   from baobab_auth_core.application.commands.authenticate_user_command import (
       AuthenticateUserCommand,
   )
   from baobab_auth_core.application.use_cases.authenticate_user import (
       AuthenticateUser,
   )

   use_case = AuthenticateUser(
       users, sessions, audit, password_hasher, token_provider,
       id_generator, clock, uow,
   )
   result = use_case.execute(
       AuthenticateUserCommand(email="alice@example.com", password="Sup3rSecret!!")
   )
   # result.tokens : TokenPair (access + refresh)
   # result.session : SessionDTO

Le message d'échec est **générique** (``InvalidCredentialsError``) : l'existence
de l'email n'est jamais divulguée. Les comptes ``DISABLED``/``DELETED``/``LOCKED``
sont refusés. Le verrouillage automatique est décrit dans :doc:`sessions`.
