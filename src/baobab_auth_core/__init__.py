"""baobab-auth-core — socle métier d'authentification et d'autorisation.

Version : 0.4.0

Ce package expose les entités, value objects, policies, ports, fakes de test,
les cas d'usage d'authentification/session, le RBAC et le catalogue
d'autorisation par défaut. Il ne contient aucune dépendance sur des technologies
concrètes (ORM, framework web, JWT, Argon2, etc.).

:spec: BL-010-001
"""

from baobab_auth_core.domain.catalogs.default_auth_catalog import (
    DefaultAuthCatalog as DefaultAuthCatalog,
)

__version__ = "0.4.0"
__all__ = ["DefaultAuthCatalog", "__version__"]
