"""Tests du cas d'usage ListRoles.

:spec: BL-050-007
"""

from baobab_auth_core.application.use_cases.list_roles import ListRoles
from baobab_auth_core.domain.value_objects.role_name import RoleName


class TestListRoles:
    def test_BL_050_007_1_liste_les_roles(  # type: ignore[no-untyped-def]
        self, roles, make_role
    ) -> None:
        roles.save(make_role("USER"))
        roles.save(make_role("ADMIN"))
        result = ListRoles(roles).execute()
        names = {r.name for r in result}
        assert {RoleName("USER"), RoleName("ADMIN")} <= names

    def test_BL_050_007_2_liste_vide(self, roles) -> None:  # type: ignore[no-untyped-def]
        assert ListRoles(roles).execute() == ()
