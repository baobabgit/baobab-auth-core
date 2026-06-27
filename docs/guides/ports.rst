Ports (protocoles)
==================

.. spec: BL-010-006

Les ports définissent les **frontières de la couche domaine** via des
``typing.Protocol`` décorés ``@runtime_checkable``. Le code métier ne connaît
que ces interfaces — jamais les implémentations concrètes.

Vue d'ensemble
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Port
     - Rôle
   * - ``Clock``
     - Fournit l'heure courante (``now() -> datetime``).
   * - ``IdGenerator``
     - Génère des identifiants uniques (``generate() -> str``).
   * - ``PasswordHasher``
     - Hache et vérifie les mots de passe.
   * - ``TokenProvider``
     - Génère et vérifie les tokens d'accès.
   * - ``UserRepository``
     - Persistance des entités ``User``.
   * - ``RoleRepository``
     - Persistance des entités ``Role``.
   * - ``PermissionRepository``
     - Persistance des entités ``Permission``.
   * - ``SessionRepository``
     - Persistance des entités ``Session``.
   * - ``AuditRepository``
     - Persistance des ``AuditEvent``.
   * - ``UnitOfWork``
     - Délimite une transaction (context manager).

Détail des interfaces
---------------------

``Clock``
~~~~~~~~~

.. code-block:: python

    class Clock(Protocol):
        def now(self) -> datetime: ...

``IdGenerator``
~~~~~~~~~~~~~~~

.. code-block:: python

    class IdGenerator(Protocol):
        def generate(self) -> str: ...

``PasswordHasher``
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class PasswordHasher(Protocol):
        def hash(self, password: PlainPassword) -> PasswordHash: ...
        def verify(self, password: PlainPassword, hashed: PasswordHash) -> bool: ...

``TokenProvider``
~~~~~~~~~~~~~~~~~

.. code-block:: python

    class TokenProvider(Protocol):
        def generate_token_id(self) -> TokenId: ...
        def create_access_token(
            self, subject: AuthSubject, token_id: TokenId, expires_at: datetime
        ) -> str: ...
        def verify_access_token(self, raw_token: str) -> AuthSubject: ...

``UserRepository``
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class UserRepository(Protocol):
        def get_by_id(self, user_id: UserId) -> User | None: ...
        def get_by_email(self, email: Email) -> User | None: ...
        def get_by_auth_subject(self, subject: AuthSubject) -> User | None: ...
        def save(self, user: User) -> None: ...
        def delete(self, user_id: UserId) -> None: ...
        def exists_by_email(self, email: Email) -> bool: ...

Les autres repositories (``RoleRepository``, ``PermissionRepository``,
``SessionRepository``) suivent le même patron : ``get_by_id``, ``save``,
``delete``, plus des méthodes de recherche spécifiques.

``AuditRepository``
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class AuditRepository(Protocol):
        def append(self, event: AuditEvent) -> None: ...
        def list_by_user(self, user_id: UserId) -> list[AuditEvent]: ...

``UnitOfWork``
~~~~~~~~~~~~~~

.. code-block:: python

    class UnitOfWork(Protocol):
        def __enter__(self) -> UnitOfWork: ...
        def __exit__(self, ...) -> None: ...
        def commit(self) -> None: ...
        def rollback(self) -> None: ...

Implémenter un port
-------------------

Pour adapter ``baobab-auth-core`` à une infrastructure concrète, implémentez
le protocole dans votre projet consommateur :

.. code-block:: python

    from datetime import datetime, UTC
    from baobab_auth_core.ports.clock import Clock

    class SystemClock:
        def now(self) -> datetime:
            return datetime.now(UTC)

    # Vérification à l'exécution (runtime_checkable)
    assert isinstance(SystemClock(), Clock)

L'utilisation de ``@runtime_checkable`` garantit que ``isinstance`` fonctionne
sans héritage explicite — duck typing structurel.
