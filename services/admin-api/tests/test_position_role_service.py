from fastapi import HTTPException
import pytest

from app.position_roles.constants import AGENT_CAPABILITY_KEYS
from app.position_roles.service import PositionRoleService, normalized_capabilities


def test_capabilities_are_restricted_to_the_governed_catalog() -> None:
    value = normalized_capabilities({"content_generation": True, "unknown": True})

    assert set(value) == set(AGENT_CAPABILITY_KEYS)
    assert value["content_generation"] is True
    assert value["code_generation"] is False


def test_role_document_only_contains_macro_capabilities() -> None:
    document = PositionRoleService._document(
        "tenant-a",
        {
            "name": "全资源岗位",
            "toolAccessMode": "all",
            "toolIds": ["old-tool"],
            "skillAccessMode": "all",
            "skillIds": ["old-skill"],
        },
    )

    assert "tool_ids" not in document
    assert "skill_ids" not in document
    assert "tool_access_mode" not in document
    assert "skill_access_mode" not in document


def test_role_name_is_required_after_trimming() -> None:
    with pytest.raises(HTTPException, match="岗位角色名称不能为空"):
        PositionRoleService._document("tenant-a", {"name": "   "})
