"""Tenant resource management & retrieval module (skeleton stage).

Public API:
- :class:`TenantResource` — the resource data model
- :class:`ResourceRepository` — the storage contract
- :class:`InMemoryResourceRepository` — the default in-memory implementation
"""

from nexent.resources.memory import InMemoryResourceRepository
from nexent.resources.models import SUPPORTED_RESOURCE_TYPES, TenantResource
from nexent.resources.repository import ResourceRepository

__all__ = [
    "InMemoryResourceRepository",
    "ResourceRepository",
    "SUPPORTED_RESOURCE_TYPES",
    "TenantResource",
]
