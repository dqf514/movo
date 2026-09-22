import asyncio
from types import SimpleNamespace

from app.product.extensions import community_extension
from app.product import resource_lifecycle


def test_community_admin_extension_has_unlimited_members_and_no_billing() -> None:
    extension = community_extension()

    assert extension.edition == "community"
    assert extension.routers == ()
    assert extension.organization_defaults["billing_enabled"] is False
    assert extension.organization_defaults["user_limit"] is None
    assert extension.resource_created == ()
    assert extension.resource_deleted == ()


def test_resource_lifecycle_notifies_sync_and_async_extension_callbacks(monkeypatch) -> None:
    calls: list[tuple[str, str, str, str]] = []

    def sync_callback(resource_type: str, main_id: str, resource_id: str) -> None:
        calls.append(("sync", resource_type, main_id, resource_id))

    async def async_callback(resource_type: str, main_id: str, resource_id: str) -> None:
        calls.append(("async", resource_type, main_id, resource_id))

    extension = SimpleNamespace(
        resource_created=(sync_callback, async_callback),
        resource_deleted=(),
    )
    monkeypatch.setattr(resource_lifecycle, "get_admin_product_extension", lambda: extension)

    asyncio.run(resource_lifecycle.notify_resource_created("skill", "tenant", "resource"))

    assert calls == [
        ("sync", "skill", "tenant", "resource"),
        ("async", "skill", "tenant", "resource"),
    ]
