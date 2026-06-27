Tests et fakes
==============

.. spec: BL-010-007, BL-010-008

``baobab-auth-core`` embarque un sous-package ``baobab_auth_core.testing`` contenant
des implémentations de test pour tous les ports. Ils permettent d'écrire des tests
unitaires déterministes sans dépendance externe.

Fakes disponibles
-----------------

``FakeClock``
~~~~~~~~~~~~~

Horloge contrôlable par les tests.

.. code-block:: python

    from baobab_auth_core.testing.fake_clock import FakeClock
    from datetime import datetime, UTC

    clock = FakeClock()                    # démarre à datetime(2024, 1, 1, tzinfo=UTC)
    clock.set_now(datetime(2025, 6, 1, tzinfo=UTC))
    clock.advance(seconds=3600)            # avance d'une heure
    print(clock.now())                     # 2025-06-01 01:00:00+00:00

``FakeIdGenerator``
~~~~~~~~~~~~~~~~~~~

Génère des identifiants prévisibles sous la forme ``"<préfixe>-<n>"``.

.. code-block:: python

    from baobab_auth_core.testing.fake_id_generator import FakeIdGenerator

    gen = FakeIdGenerator(prefix="user")
    assert gen.generate() == "user-1"
    assert gen.generate() == "user-2"
    gen.reset()
    assert gen.generate() == "user-1"

``FakePasswordHasher``
~~~~~~~~~~~~~~~~~~~~~~

Hache avec le préfixe ``"hashed:"`` — ne fait aucune cryptographie.

.. code-block:: python

    from baobab_auth_core.testing.fake_password_hasher import FakePasswordHasher
    from baobab_auth_core.domain.value_objects.plain_password import PlainPassword
    from baobab_auth_core.domain.value_objects.password_hash import PasswordHash

    hasher = FakePasswordHasher()
    plain = PlainPassword("s3cr3t!")
    hashed = hasher.hash(plain)                    # PasswordHash("hashed:s3cr3t!")
    assert hasher.verify(plain, hashed) is True
    assert hasher.verify(PlainPassword("wrong"), hashed) is False

``FakeTokenProvider``
~~~~~~~~~~~~~~~~~~~~~

Génère des tokens de la forme ``"fake-token:<subject>"``.
Markers spéciaux pour simuler les cas d'erreur :

- ``"fake-token:EXPIRED:<subject>"`` → lève ``TokenExpiredError`` à la vérification.
- ``"fake-token:INVALID:<subject>"`` → lève ``TokenInvalidError``.

.. code-block:: python

    from baobab_auth_core.testing.fake_token_provider import FakeTokenProvider
    from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
    from baobab_auth_core.exceptions.auth import TokenExpiredError

    provider = FakeTokenProvider()
    subject = AuthSubject("user-42")
    token = provider.create_access_token(subject, token_id, expires_at)
    # "fake-token:user-42"

    expired = "fake-token:EXPIRED:user-42"
    try:
        provider.verify_access_token(expired)
    except TokenExpiredError:
        pass

Repositories en mémoire
------------------------

Cinq repositories en mémoire (``dict``-based) implémentent les ports correspondants.
Chacun expose une méthode ``clear()`` pour réinitialiser l'état entre les tests.

- ``InMemoryUserRepository``
- ``InMemoryRoleRepository``
- ``InMemoryPermissionRepository``
- ``InMemorySessionRepository``
- ``InMemoryAuditRepository`` (``list``-based ; propriété ``all_events``)

.. code-block:: python

    from baobab_auth_core.testing.in_memory_user_repository import InMemoryUserRepository
    from baobab_auth_core.testing.in_memory_audit_repository import InMemoryAuditRepository

    user_repo = InMemoryUserRepository()
    user_repo.save(user)
    found = user_repo.get_by_email(user.email)
    assert found is not None

    audit_repo = InMemoryAuditRepository()
    audit_repo.append(event)
    assert len(audit_repo.all_events) == 1

``InMemoryUnitOfWork``
~~~~~~~~~~~~~~~~~~~~~~

Suit les appels ``commit()`` et ``rollback()`` ; lève ``RuntimeError`` si appelés
hors contexte.

.. code-block:: python

    from baobab_auth_core.testing.in_memory_unit_of_work import InMemoryUnitOfWork

    uow = InMemoryUnitOfWork()
    with uow:
        # ... opérations ...
        uow.commit()

    assert uow.committed is True
    assert uow.rolled_back is False

Builders de fixtures
--------------------

Le module ``tests/fixtures/builders.py`` fournit des fonctions ``make_*`` pour
construire des entités avec des valeurs par défaut sensées :

.. code-block:: python

    from tests.fixtures.builders import make_user, make_role, make_session

    user = make_user()           # User PENDING, rôles vides
    user = make_user(status=UserStatus.ACTIVE, roles=[RoleName("ADMIN")])
    role = make_role(name=RoleName("EDITOR"))
    session = make_session(user_id=user.id)

Structure des tests
-------------------

Les tests suivent la structure **AAA** (Arrange / Act / Assert) et l'arborescence
miroir ``src/<pkg>/a/b/c.py`` → ``tests/unit/<pkg>/a/b/test_c.py``.

Les noms de test portent l'identifiant de spécification :
``def test_BL_010_002_1_cas_nominal(...)``.

Conventions d'assertion pour les value objects :

- Mutations sur frozen dataclass → ``pytest.raises(dataclasses.FrozenInstanceError)``
- Validation → ``pytest.raises(<ExceptionConcrète>)``
- Masquage → ``assert "secret" not in str(obj)``
