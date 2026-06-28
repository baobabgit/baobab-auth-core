"""Contrat ``admin`` — cas d'usage d'administration.

N'importe que ``baobab_auth_core``.

:spec: BL-050-009
"""

import baobab_auth_core as core


class TestAdminContract:
    def test_BL_050_009_1_cas_usage_admin_exposes(self) -> None:
        for name in (
            "BootstrapSuperAdmin",
            "DisableUser",
            "EnableUser",
            "RequestJwkRotation",
            "ListRoles",
            "ListPermissions",
            "ListUserSessions",
        ):
            assert hasattr(core, name)
