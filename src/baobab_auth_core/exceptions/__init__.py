"""Hiérarchie d'exceptions métier de baobab-auth-core.

:spec: BL-010-005
"""

from baobab_auth_core.exceptions.auth import (
    InvalidCredentialsError as InvalidCredentialsError,
)
from baobab_auth_core.exceptions.auth import (
    TokenExpiredError as TokenExpiredError,
)
from baobab_auth_core.exceptions.auth import (
    TokenInvalidError as TokenInvalidError,
)
from baobab_auth_core.exceptions.authorization import (
    AuthorizationError as AuthorizationError,
)
from baobab_auth_core.exceptions.authorization import (
    ForbiddenError as ForbiddenError,
)
from baobab_auth_core.exceptions.authorization import (
    PermissionDeniedError as PermissionDeniedError,
)
from baobab_auth_core.exceptions.base import BaobabAuthCoreError as BaobabAuthCoreError
from baobab_auth_core.exceptions.role import (
    LastAdminRoleRemovalError as LastAdminRoleRemovalError,
)
from baobab_auth_core.exceptions.role import (
    LastSuperAdminRoleRemovalError as LastSuperAdminRoleRemovalError,
)
from baobab_auth_core.exceptions.role import (
    PermissionNotFoundError as PermissionNotFoundError,
)
from baobab_auth_core.exceptions.role import (
    RoleError as RoleError,
)
from baobab_auth_core.exceptions.role import (
    RoleNotFoundError as RoleNotFoundError,
)
from baobab_auth_core.exceptions.session import (
    SessionExpiredError as SessionExpiredError,
)
from baobab_auth_core.exceptions.session import (
    SessionNotFoundError as SessionNotFoundError,
)
from baobab_auth_core.exceptions.session import (
    SessionRevokedError as SessionRevokedError,
)
from baobab_auth_core.exceptions.user import (
    UserAlreadyExistsError as UserAlreadyExistsError,
)
from baobab_auth_core.exceptions.user import (
    UserDeletedError as UserDeletedError,
)
from baobab_auth_core.exceptions.user import (
    UserDisabledError as UserDisabledError,
)
from baobab_auth_core.exceptions.user import (
    UserLockedError as UserLockedError,
)
from baobab_auth_core.exceptions.user import (
    UserNotFoundError as UserNotFoundError,
)
from baobab_auth_core.exceptions.validation import (
    InvalidEmailError as InvalidEmailError,
)
from baobab_auth_core.exceptions.validation import (
    InvalidPermissionNameError as InvalidPermissionNameError,
)
from baobab_auth_core.exceptions.validation import (
    InvalidRoleNameError as InvalidRoleNameError,
)
from baobab_auth_core.exceptions.validation import (
    ValidationError as ValidationError,
)
from baobab_auth_core.exceptions.validation import (
    WeakPasswordError as WeakPasswordError,
)

__all__ = [
    "AuthorizationError",
    "BaobabAuthCoreError",
    "ForbiddenError",
    "InvalidCredentialsError",
    "InvalidEmailError",
    "InvalidPermissionNameError",
    "InvalidRoleNameError",
    "LastAdminRoleRemovalError",
    "LastSuperAdminRoleRemovalError",
    "PermissionDeniedError",
    "PermissionNotFoundError",
    "RoleError",
    "RoleNotFoundError",
    "SessionExpiredError",
    "SessionNotFoundError",
    "SessionRevokedError",
    "TokenExpiredError",
    "TokenInvalidError",
    "UserAlreadyExistsError",
    "UserDeletedError",
    "UserDisabledError",
    "UserLockedError",
    "UserNotFoundError",
    "ValidationError",
    "WeakPasswordError",
]
