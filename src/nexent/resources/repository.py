"""Storage contract for tenant resource management & retrieval (skeleton stage).

Future backends (Elasticsearch, Milvus, ...) must implement this interface —
mirroring the abstract-base style of the upstream ``VectorDatabaseCore``.
"""

from abc import ABC, abstractmethod

from nexent.resources.models import TenantResource


class ResourceRepository(ABC):
    """Persistence contract for per-tenant resource storage and retrieval."""

    @abstractmethod
    def add(self, resource: TenantResource) -> TenantResource:
        """Store ``resource``; generate ``resource_id`` when empty.

        Returns:
            The stored resource (with generated id, if applicable).

        Raises:
            ValueError: If a resource with the same (tenant_id, resource_id)
                already exists.
        """

    @abstractmethod
    def get(self, tenant_id: str, resource_id: str) -> TenantResource | None:
        """Return the resource for ``(tenant_id, resource_id)`` or ``None``."""

    @abstractmethod
    def list_by_tenant(self, tenant_id: str) -> list[TenantResource]:
        """Return all resources of a tenant (insertion order)."""

    @abstractmethod
    def search(
        self,
        tenant_id: str,
        query: str,
        resource_type: str | None = None,
    ) -> list[TenantResource]:
        """Search a tenant's resources by keyword (case-insensitive substring).

        Args:
            tenant_id: Tenant scope.
            query: Keyword; empty query matches all of the tenant's resources.
            resource_type: Optional filter on resource type.

        Returns:
            Matching resources in insertion order.
        """

    @abstractmethod
    def delete(self, tenant_id: str, resource_id: str) -> bool:
        """Delete a resource; return True when it existed and was removed."""

    @abstractmethod
    def count(self, tenant_id: str) -> int:
        """Return the number of stored resources for a tenant."""
