"""Contract tests for the ResourceRepository interface (skeleton stage).

Any future storage backend (Elasticsearch, Milvus, ...) must satisfy this
contract; the in-memory implementation in ``nexent.resources.memory`` is the
reference for tests in the skeleton stage.
"""

from datetime import UTC, datetime

from nexent.resources import ResourceRepository, TenantResource
from nexent.resources.memory import InMemoryResourceRepository


def test_public_api_exports_resource_repository_and_model():
    assert issubclass(InMemoryResourceRepository, ResourceRepository)
    assert hasattr(TenantResource, "matches_query")


def test_memory_repository_satisfies_interface_contract():
    repo: ResourceRepository = InMemoryResourceRepository()

    stored = repo.add(
        TenantResource(
            tenant_id="tenant-a",
            resource_id="res-001",
            resource_type="document",
            content="tenant resource",
            created_at=datetime.now(UTC),
        )
    )

    assert repo.get("tenant-a", stored.resource_id) is not None
    assert repo.count("tenant-a") == 1
    assert repo.search("tenant-a", "resource") == [stored]
    assert repo.delete("tenant-a", stored.resource_id) is True
    assert repo.count("tenant-a") == 0
