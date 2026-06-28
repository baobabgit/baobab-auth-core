"""Contrat ``api`` — cas d'usage couvrant les endpoints attendus.

Ce test n'importe **que** ``baobab_auth_core`` et vérifie que le core ne lève
jamais d'exception web (les exceptions héritent de ``BaobabAuthCoreError``).

:spec: BL-050-009
"""

import baobab_auth_core as core
from baobab_auth_core.exceptions.base import BaobabAuthCoreError

# endpoint → cas d'usage du core
_ENDPOINT_USE_CASES = {
    "POST /auth/register": "RegisterUser",
    "POST /auth/login": "AuthenticateUser",
    "POST /auth/refresh": "RefreshSession",
    "POST /auth/logout": "Logout",
    "GET /auth/me": "GetCurrentUser",
    "GET /auth/roles": "ListRoles",
    "GET /auth/permissions": "ListPermissions",
    "GET /auth/sessions": "ListUserSessions",
    "POST /auth/sessions/{id}/revoke": "RevokeSession",
    "POST /auth/users/{id}/roles": "AssignRole",
    "DELETE /auth/users/{id}/roles/{role}": "RemoveRole",
    "POST /auth/users/{id}/disable": "DisableUser",
    "POST /auth/users/{id}/enable": "EnableUser",
    "POST /auth/jwks/rotation-request": "RequestJwkRotation",
}


class TestApiContract:
    def test_BL_050_009_1_cas_usage_par_endpoint(self) -> None:
        for endpoint, use_case in _ENDPOINT_USE_CASES.items():
            assert hasattr(core, use_case), f"{endpoint} -> {use_case} manquant"

    def test_BL_050_009_2_exceptions_avec_error_code_et_http_status(self) -> None:
        # Le core fournit error_code + http_status sans dépendre d'un framework web.
        assert BaobabAuthCoreError.error_code == "auth.error"
        assert isinstance(BaobabAuthCoreError.http_status, int)
        assert not any(
            base.__name__ == "HTTPException" for base in BaobabAuthCoreError.__mro__
        )
