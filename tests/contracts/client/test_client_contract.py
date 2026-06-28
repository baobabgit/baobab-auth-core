"""Contrat ``client`` — types de lecture côté client.

Le client ne recalcule pas les permissions depuis les rôles : ``AuthContext`` et
``AuthenticatedUser`` les exposent directement. N'importe que ``baobab_auth_core``.

:spec: BL-050-009
"""

import dataclasses

import baobab_auth_core as core
from baobab_auth_core import AuthContext, AuthenticatedUser


class TestClientContract:
    def test_BL_050_009_1_types_client_exposes(self) -> None:
        for name in (
            "AuthSubject",
            "AuthContext",
            "AuthenticatedUser",
            "TokenClaims",
            "RoleName",
            "PermissionName",
        ):
            assert hasattr(core, name)

    def test_BL_050_009_2_permissions_disponibles_sans_recalcul(self) -> None:
        ctx_fields = {f.name for f in dataclasses.fields(AuthContext)}
        user_fields = {f.name for f in dataclasses.fields(AuthenticatedUser)}
        assert "permissions" in ctx_fields
        assert "permissions" in user_fields
        # accès public ``roles`` sur AuthenticatedUser
        assert hasattr(AuthenticatedUser, "roles")
