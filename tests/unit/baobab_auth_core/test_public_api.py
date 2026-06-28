"""Tests de l'API publique (exports stabilisés).

:spec: BL-050-001
"""

import baobab_auth_core


class TestPublicApi:
    def test_BL_050_001_1_tous_les_symboles_importables(self) -> None:
        for name in baobab_auth_core.__all__:
            assert hasattr(baobab_auth_core, name), f"Symbole manquant : {name}"

    def test_BL_050_001_2_all_trie_et_sans_doublon(self) -> None:
        names = baobab_auth_core.__all__
        assert len(names) == len(set(names))

    def test_BL_050_001_3_contrat_minimal_present(self) -> None:
        required = {
            "User",
            "Role",
            "Permission",
            "Session",
            "AuditEvent",
            "UserProfile",
            "Email",
            "AuthSubject",
            "PlainPassword",
            "PasswordHash",
            "RoleName",
            "PermissionName",
            "SessionId",
            "TokenId",
            "UserStatus",
            "SessionStatus",
            "AuditEventType",
            "AuditSeverity",
            "PasswordPolicy",
            "SessionPolicy",
            "RolePolicy",
            "PermissionPolicy",
            "LockoutPolicy",
            "DefaultAuthCatalog",
            "UserRepository",
            "RoleRepository",
            "PermissionRepository",
            "SessionRepository",
            "AuditRepository",
            "PasswordHasher",
            "TokenProvider",
            "Clock",
            "IdGenerator",
            "UnitOfWork",
            "AuthContext",
            "AuthenticatedUser",
            "TokenPair",
            "TokenClaims",
            "SessionDTO",
            "TokenIssueContext",
            "RegisterUser",
            "AuthenticateUser",
            "RefreshSession",
            "Logout",
            "RevokeSession",
            "RevokeAllSessions",
            "AssignRole",
            "RemoveRole",
            "ChangePassword",
        }
        assert required <= set(baobab_auth_core.__all__)

    def test_BL_050_001_4_version_exposee(self) -> None:
        assert baobab_auth_core.__version__ == "0.5.0"
