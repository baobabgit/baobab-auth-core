"""Contrat ``security`` — hachage, tokens et contexte d'émission.

Ce test n'importe **que** ``baobab_auth_core``.

:spec: BL-050-009
"""

import dataclasses

import baobab_auth_core as core
from baobab_auth_core import TokenClaims, TokenIssueContext


class TestSecurityContract:
    def test_BL_050_009_1_ports_security_exposes(self) -> None:
        for name in ("PasswordHasher", "TokenProvider", "TokenPair", "TokenClaims"):
            assert hasattr(core, name)

    def test_BL_050_009_2_token_issue_context_champs(self) -> None:
        fields = {f.name for f in dataclasses.fields(TokenIssueContext)}
        assert {
            "subject",
            "user_id",
            "session_id",
            "roles",
            "permissions",
            "issued_at",
            "access_expires_at",
            "refresh_expires_at",
            "issuer",
            "audience",
        } <= fields

    def test_BL_050_009_3_claims_mapping_sub_jti_sid(self) -> None:
        fields = {f.name for f in dataclasses.fields(TokenClaims)}
        # sub=subject, jti=token_id, sid=session_id
        assert {"subject", "token_id", "session_id"} <= fields
