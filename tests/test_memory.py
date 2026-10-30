"""Unit tests for nexent.resources.memory — in-memory repository implementation."""

from datetime import UTC, datetime, timedelta

import pytest

from nexent.resources.memory import InMemoryResourceRepository
from nexent.resources.models import TenantResource


def make_resource(tenant_id="tenant-a", resource_id="res-001", content="text"):
    return TenantResource(
        tenant_id=tenant_id,
        resource_id=resource_id,
        resource_type="document",
        content=content,
        created_at=datetime.now(UTC),
    )


class TestInMemoryRepositoryAdd:
    def test_add_returns_resource_with_generated_id(self):
        repo = InMemoryResourceRepository()

        stored = repo.add(make_resource(resource_id=""))

        assert stored.resource_id != ""
        assert stored.resource_id.startswith("res-")

    def test_add_rejects_duplicate_resource_id(self):
        repo = InMemoryResourceRepository()
        repo.add(make_resource(resource_id="res-001"))

        with pytest.raises(ValueError, match="already exists"):
            repo.add(make_resource(resource_id="res-001"))


class TestInMemoryRepositoryQuery:
    def test_list_by_tenant_isolation(self):
        repo = InMemoryResourceRepository()
        repo.add(make_resource(tenant_id="tenant-a", content="alpha"))
        repo.add(make_resource(tenant_id="tenant-b", content="beta"))

        results = repo.list_by_tenant("tenant-a")

        assert len(results) == 1
        assert results[0].tenant_id == "tenant-a"

    def test_search_filters_by_content_keyword(self):
        repo = InMemoryResourceRepository()
        repo.add(make_resource(resource_id="r1", content="quarterly report"))
        repo.add(make_resource(resource_id="r2", content="monthly summary"))

        results = repo.search("tenant-a", "quarterly")

        assert len(results) == 1
        assert results[0].resource_id == "r1"

    def test_search_filters_by_resource_type(self):
        repo = InMemoryResourceRepository()
        repo.add(make_resource(resource_id="r1", content="report"))
        repo.add(make_resource(resource_id="r2", content="report"))

        results = repo.search("tenant-a", "report", resource_type="image")

        assert results == []


class TestInMemoryRepositoryDelete:
    def test_delete_removes_resource_and_returns_true(self):
        repo = InMemoryResourceRepository()
        repo.add(make_resource(resource_id="res-001"))

        assert repo.delete("tenant-a", "res-001") is True
        assert repo.list_by_tenant("tenant-a") == []

    def test_delete_missing_resource_returns_false(self):
        repo = InMemoryResourceRepository()

        assert repo.delete("tenant-a", "nope") is False


class TestInMemoryRepositoryGet:
    def test_get_returns_stored_resource(self):
        repo = InMemoryResourceRepository()
        original = make_resource(resource_id="res-001")
        repo.add(original)

        fetched = repo.get("tenant-a", "res-001")

        assert fetched == original

    def test_get_returns_none_when_missing(self):
        repo = InMemoryResourceRepository()

        assert repo.get("tenant-a", "nope") is None

    def test_get_is_tenant_scoped(self):
        repo = InMemoryResourceRepository()
        repo.add(make_resource(tenant_id="tenant-a", resource_id="res-001"))

        assert repo.get("tenant-b", "res-001") is None


class TestInMemoryRepositoryCount:
    def test_count_reflects_stored_resources_per_tenant(self):
        repo = InMemoryResourceRepository()
        repo.add(make_resource(resource_id="r1"))
        repo.add(make_resource(resource_id="r2"))
        repo.add(make_resource(tenant_id="tenant-b", resource_id="r3"))

        assert repo.count("tenant-a") == 2
        assert repo.count("tenant-b") == 1

    def test_created_at_preserved_within_tolerance(self):
        before = datetime.now(UTC)
        repo = InMemoryResourceRepository()
        repo.add(make_resource(resource_id="r1"))

        stored = repo.get("tenant-a", "r1")

        # Time-range assertion per project spec (no millisecond equality).
        assert before <= stored.created_at <= before + timedelta(seconds=5)
