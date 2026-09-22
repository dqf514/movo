from __future__ import annotations

import asyncio

import pytest

from app.api.endpoints import models as model_endpoints
from app.api.principal import ApiPrincipal
from app.dsh_runtime.profile.compiler import ModelProfileCompiler


class Catalog:
    def __init__(self) -> None:
        self.selected: str | None = None

    async def resolve(self, tenant_id: str, model_instance_id: str | None):
        self.selected = model_instance_id
        return (
            {
                "_id": model_instance_id,
                "main_id": tenant_id,
                "provider_id": "provider-a",
                "model_name": "allowed-model",
                "display_name": "Allowed Model",
                "status": "active",
                "capabilities": ["chat"],
            },
            {"_id": "provider-a", "status": "active", "provider_type": "openai_compatible"},
        )


class Policy:
    def __init__(self, selected: str = "model-allowed") -> None:
        self.selected = selected
        self.calls: list[dict[str, object]] = []

    async def resolve_model_id(self, **kwargs):
        self.calls.append(kwargs)
        return self.selected


def test_profile_compiler_resolves_an_authorized_default_for_the_user() -> None:
    async def run():
        catalog = Catalog()
        policy = Policy()
        snapshot = await ModelProfileCompiler(catalog, model_access_policy=policy).compile(
            tenant_id="tenant-a", user_id="user-a"
        )
        assert catalog.selected == "model-allowed"
        assert snapshot.model_instance_id == "model-allowed"
        assert policy.calls == [{
            "main_id": "tenant-a",
            "user_id": "user-a",
            "model_id": None,
            "capability": "chat",
        }]

    asyncio.run(run())


def test_profile_compiler_propagates_model_permission_denial() -> None:
    class DenyPolicy(Policy):
        async def resolve_model_id(self, **kwargs):
            raise PermissionError("model denied")

    async def run():
        with pytest.raises(PermissionError, match="model denied"):
            await ModelProfileCompiler(Catalog(), model_access_policy=DenyPolicy()).compile(
                tenant_id="tenant-a", user_id="user-a", model_instance_id="model-denied"
            )

    asyncio.run(run())


def test_available_models_are_filtered_with_the_authenticated_principal(monkeypatch) -> None:
    class FilterPolicy:
        async def filter_options(self, **kwargs):
            assert kwargs["main_id"] == "tenant-a"
            assert kwargs["user_id"] == "user-a"
            return [kwargs["options"][1]]

    async def list_options(main_id: str):
        assert main_id == "tenant-a"
        return [{"id": "finance"}, {"id": "hr"}]

    monkeypatch.setattr(model_endpoints, "list_chat_model_options", list_options)
    monkeypatch.setattr(
        model_endpoints,
        "get_product_extension",
        lambda: type("Extension", (), {"model_access_policy": FilterPolicy()})(),
    )

    result = asyncio.run(model_endpoints.available_models(
        main_id="ignored-client-tenant",
        capability="chat",
        principal=ApiPrincipal(kind="end_user", main_id="tenant-a", user_id="user-a"),
    ))
    assert result["data"] == [{"id": "hr"}]
