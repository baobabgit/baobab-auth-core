# Contrat — Imports publics

> Imports garantis stables pour les consommateurs de ce package.

## Imports garantis

```python
from baobab_auth_core import __version__
from baobab_auth_core.application.results import AuthContext
from baobab_auth_core.application.services import AuthorizationService
from baobab_auth_core.domain.entities import AuditEvent, Permission, Role, Session, User
from baobab_auth_core.domain.enums import AuditEventType, AuditSeverity, SessionStatus
from baobab_auth_core.domain.policies import PasswordPolicy, PermissionPolicy, RolePolicy
from baobab_auth_core.domain.value_objects import AuthSubject, PermissionName, RoleName
from baobab_auth_core.exceptions import ForbiddenError, PermissionDeniedError, RoleError
from baobab_auth_core.ports import PermissionRepository, RoleRepository, UserRepository
from baobab_auth_core.testing import InMemoryPermissionRepository, InMemoryRoleRepository
```

## Imports internes (non garantis)

Les sous-modules non exportés dans `__all__` sont considérés comme internes
et peuvent changer sans bump majeur.
