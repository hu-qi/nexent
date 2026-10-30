"""Unit tests for nexent.resources.models — TenantResource data model."""

from datetime import UTC, datetime, timedelta

import pytest

from nexent.resources.models import TenantResource


class TestTenantResourceCreation:
    def test_creates_resource_with_all_fields(self):
        created = datetime(2026, 1, 1, 12, 0, 0, tzinfo=UTC)

        resource = TenantResource(
            tenant_id="tenant-a",
            resource_id="res-001",
            resource_type="document",
            content=" quarterly report ",
            created_at=created,
        )

        assert resource.tenant_id == "tenant-a"
        assert resource.resource_id == "res-001"
        assert resource.resource_type == "document"
        assert resource.content == "quarterly report"
        assert resource.created_at == created


class TestTenantResourceValidation:
    def test_rejects_empty_tenant_id(self):
        with pytest.raises(ValueError, match="tenant_id"):
            TenantResource(
                tenant_id="",
                resource_id="res-001",
                resource_type="document",
                content="text",
                created_at=datetime.now(UTC),
            )

    def test_whitespace_resource_id_normalizes_to_generate_sentinel(self):
        # resource_id="" (and whitespace, after normalization) means
        # "let the repository generate an id on add()".
        resource = TenantResource(
            tenant_id="tenant-a",
            resource_id="   ",
            resource_type="document",
            content="text",
            created_at=datetime.now(UTC),
        )

        assert resource.resource_id == ""

    def test_rejects_blank_content(self):
        with pytest.raises(ValueError, match="content"):
            TenantResource(
                tenant_id="tenant-a",
                resource_id="res-001",
                resource_type="document",
                content="   ",
                created_at=datetime.now(UTC),
            )

    def test_rejects_unknown_resource_type(self):
        with pytest.raises(ValueError, match="resource_type"):
            TenantResource(
                tenant_id="tenant-a",
                resource_id="res-001",
                resource_type="hologram",
                content="text",
                created_at=datetime.now(UTC),
            )

    def test_default_created_at_is_now_utc(self):
        before = datetime.now(UTC)

        resource = TenantResource(
            tenant_id="tenant-a",
            resource_id="res-001",
            resource_type="document",
            content="text",
        )

        # Time-range assertion (never millisecond equality) per project spec.
        assert before <= resource.created_at <= before + timedelta(seconds=5)


class TestTenantResourceMethods:
    def test_matches_query_is_case_insensitive(self):
        resource = TenantResource(
            tenant_id="tenant-a",
            resource_id="res-001",
            resource_type="document",
            content="Quarterly Report",
            created_at=datetime.now(UTC),
        )

        assert resource.matches_query("quarterly") is True
        assert resource.matches_query("REPORT") is True
        assert resource.matches_query("monthly") is False

    def test_matches_query_on_empty_query_returns_true(self):
        resource = TenantResource(
            tenant_id="tenant-a",
            resource_id="res-001",
            resource_type="document",
            content="text",
            created_at=datetime.now(UTC),
        )

        assert resource.matches_query("") is True

    def test_to_dict_roundtrips_via_from_dict(self):
        resource = TenantResource(
            tenant_id="tenant-a",
            resource_id="res-001",
            resource_type="document",
            content="text",
            created_at=datetime(2026, 1, 1, 12, 0, 0, tzinfo=UTC),
        )

        restored = TenantResource.from_dict(resource.to_dict())

        assert restored == resource
