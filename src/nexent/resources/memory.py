"""In-memory :class:`ResourceRepository` implementation (skeleton-stage default)."""

import uuid

from nexent.resources.models import TenantResource
from nexent.resources.repository import ResourceRepository


class InMemoryResourceRepository(ResourceRepository):
    """Reference implementation kept in process memory — per-tenant scoped.

    Suitable for tests, examples and local dry runs; swap for a persistent
    backend (e.g. Elasticsearch) in production.
    """

    def __init__(self) -> None:
        # Keyed by (tenant_id, resource_id) to enforce tenant isolation.
        self._resources: dict[tuple[str, str], TenantResource] = {}
        self._order: list[tuple[str, str]] = []

    def add(self, resource: TenantResource) -> TenantResource:
        stored = resource
        if not stored.resource_id:
            generated = f"res-{uuid.uuid4().hex[:12]}"
            stored = TenantResource(
                tenant_id=resource.tenant_id,
                resource_id=generated,
                resource_type=resource.resource_type,
                content=resource.content,
                created_at=resource.created_at,
            )

        key = (stored.tenant_id, stored.resource_id)
        if key in self._resources:
            raise ValueError(f"resource {stored.resource_id!r} already exists for tenant {stored.tenant_id!r}")

        self._resources[key] = stored
        self._order.append(key)
        return stored

    def get(self, tenant_id: str, resource_id: str) -> TenantResource | None:
        return self._resources.get((tenant_id, resource_id))

    def list_by_tenant(self, tenant_id: str) -> list[TenantResource]:
        return [self._resources[k] for k in self._order if k[0] == tenant_id]

    def search(
        self,
        tenant_id: str,
        query: str,
        resource_type: str | None = None,
    ) -> list[TenantResource]:
        results = []
        for key in self._order:
            if key[0] != tenant_id:
                continue
            resource = self._resources[key]
            if resource_type is not None and resource.resource_type != resource_type:
                continue
            if resource.matches_query(query):
                results.append(resource)
        return results

    def delete(self, tenant_id: str, resource_id: str) -> bool:
        key = (tenant_id, resource_id)
        if key not in self._resources:
            return False
        del self._resources[key]
        self._order.remove(key)
        return True

    def count(self, tenant_id: str) -> int:
        return sum(1 for k in self._order if k[0] == tenant_id)
