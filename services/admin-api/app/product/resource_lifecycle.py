from __future__ import annotations

from typing import Literal

from app.product.extensions import get_admin_product_extension


ResourceType = Literal["skill", "tool"]


async def notify_resource_created(resource_type: ResourceType, main_id: str, resource_id: str) -> None:
    await _notify("resource_created", resource_type, main_id, resource_id)


async def notify_resource_deleted(resource_type: ResourceType, main_id: str, resource_id: str) -> None:
    await _notify("resource_deleted", resource_type, main_id, resource_id)


async def _notify(event: str, resource_type: ResourceType, main_id: str, resource_id: str) -> None:
    callbacks = getattr(get_admin_product_extension(), event)
    for callback in callbacks:
        result = callback(resource_type, str(main_id), str(resource_id))
        if hasattr(result, "__await__"):
            await result
