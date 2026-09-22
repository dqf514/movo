import asyncio

import pytest
from fastapi import HTTPException

from app.api.endpoints import external_tools as endpoint
from app.api.principal import ApiPrincipal


def test_end_user_registry_is_filtered_by_resource_policy(monkeypatch) -> None:
    async def list_descriptors(main_id: str):
        assert main_id == "tenant"
        return [{"id": "allowed"}, {"id": "blocked"}]

    async def filter_ids(resource_type: str, **kwargs):
        assert resource_type == "tool"
        assert kwargs["user_id"] == "user"
        return {"allowed"}

    monkeypatch.setattr(endpoint.external_tool_registry, "list_enabled_descriptors", list_descriptors)
    monkeypatch.setattr(endpoint, "filter_allowed_resource_ids", filter_ids)

    result = asyncio.run(
        endpoint.list_external_tool_registry(
            main_id="tenant",
            principal=ApiPrincipal(kind="end_user", main_id="tenant", user_id="user"),
        )
    )

    assert result.data == [{"id": "allowed"}]


def test_end_user_cannot_test_denied_organization_tool(monkeypatch) -> None:
    async def denied(*args, **kwargs):
        return False

    monkeypatch.setattr(endpoint, "resource_is_allowed", denied)

    with pytest.raises(HTTPException) as error:
        asyncio.run(
            endpoint.test_external_tool(
                "blocked",
                endpoint.ToolTestPayload(input={}),
                main_id="tenant",
                principal=ApiPrincipal(kind="end_user", main_id="tenant", user_id="user"),
            )
        )

    assert error.value.status_code == 403


def test_admin_service_can_test_organization_tool_without_employee_audience(monkeypatch) -> None:
    async def test_tool(tool_id: str, payload: dict, main_id: str):
        return {"tool": tool_id, "main": main_id}

    monkeypatch.setattr(endpoint.external_tool_service, "test", test_tool)

    result = asyncio.run(
        endpoint.test_external_tool(
            "managed-tool",
            endpoint.ToolTestPayload(input={}),
            main_id="tenant",
            principal=ApiPrincipal(kind="admin_service", main_id="tenant"),
        )
    )

    assert result.data == {"tool": "managed-tool", "main": "tenant"}
