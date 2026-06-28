"""Tests des codes d'erreur métier sur les exceptions publiques.

:spec: BL-050-003
"""

import pytest

from baobab_auth_core import exceptions as exc
from baobab_auth_core.exceptions.base import BaobabAuthCoreError

# (exception, error_code, http_status) — extrait du cahier v0.5.0 §6.
_TABLE = [
    (exc.InvalidCredentialsError, "auth.credentials.invalid", 401),
    (exc.ForbiddenError, "auth.authorization.forbidden", 403),
    (exc.PermissionDeniedError, "auth.authorization.permission_denied", 403),
    (exc.UserNotFoundError, "auth.user.not_found", 404),
    (exc.UserAlreadyExistsError, "auth.user.already_exists", 409),
    (exc.LastSuperAdminRoleRemovalError, "auth.role.last_super_admin", 409),
    (exc.UserLockedError, "auth.user.locked", 423),
]


class TestErrorCodes:
    @pytest.mark.parametrize(("exception", "code", "status"), _TABLE)
    def test_BL_050_003_1_mapping_cahier(
        self,
        exception: type[BaobabAuthCoreError],
        code: str,
        status: int,
    ) -> None:
        assert exception.error_code == code
        assert exception.http_status == status
        assert isinstance(exception.safe_message, str) and exception.safe_message

    def test_BL_050_003_2_toutes_les_exceptions_publiques_ont_un_code(self) -> None:
        public = [
            getattr(exc, name)
            for name in exc.__all__
            if isinstance(getattr(exc, name), type)
            and issubclass(getattr(exc, name), BaobabAuthCoreError)
        ]
        assert public
        for exception in public:
            assert exception.error_code.startswith("auth.")
            assert isinstance(exception.http_status, int)
            assert exception.safe_message

    def test_BL_050_003_3_codes_uniques_par_type(self) -> None:
        # Chaque code concret (hors base/alias) doit être distinct.
        codes = [
            cls.error_code
            for name in exc.__all__
            if isinstance((cls := getattr(exc, name)), type)
            and issubclass(cls, BaobabAuthCoreError)
            and cls not in (BaobabAuthCoreError,)
        ]
        # L'alias LastAdminRoleRemovalError partage le code de LastSuperAdmin.
        assert codes.count("auth.role.last_super_admin") >= 1

    def test_BL_050_003_4_safe_message_ne_fuit_pas(self) -> None:
        err = exc.InvalidCredentialsError("email=alice@example.com password=secret")
        assert "secret" not in err.safe_message
        assert err.safe_message == "Identifiants invalides."
        assert err.message == "email=alice@example.com password=secret"
