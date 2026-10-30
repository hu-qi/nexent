"""Data models for tenant resource management & retrieval (skeleton stage)."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, ClassVar

#: Resource kinds supported in the skeleton stage.
SUPPORTED_RESOURCE_TYPES = frozenset({"document", "image", "audio", "video", "table"})


@dataclass
class TenantResource:
    """A retrievable resource owned by a tenant.

    Attributes:
        tenant_id: Identifier of the owning tenant.
        resource_id: Unique resource identifier within a tenant; left empty to
            let the repository generate one on ``add()``.
        resource_type: One of :data:`SUPPORTED_RESOURCE_TYPES`.
        content: Searchable text content (stored trimmed).
        created_at: Creation timestamp; defaults to ``now`` in UTC.
    """

    tenant_id: str
    resource_id: str = ""
    resource_type: str = "document"
    content: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    __KNOWN_TYPES: ClassVar[frozenset[str]] = SUPPORTED_RESOURCE_TYPES

    def __post_init__(self) -> None:
        self.content = self.content.strip()
        self.resource_id = self.resource_id.strip()
        if not self.tenant_id:
            raise ValueError("tenant_id must not be empty")
        if not self.resource_type:
            raise ValueError("resource_type must not be empty")
        if self.resource_type not in self.__KNOWN_TYPES:
            allowed = ", ".join(sorted(self.__KNOWN_TYPES))
            raise ValueError(f"resource_type must be one of: {allowed}")
        if not self.content:
            raise ValueError("content must not be blank")

    def matches_query(self, query: str) -> bool:
        """Return True when ``query`` (case-insensitive substring) hits the content."""
        if not query:
            return True
        return query.lower() in self.content.lower()

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dict."""
        return {
            "tenant_id": self.tenant_id,
            "resource_id": self.resource_id,
            "resource_type": self.resource_type,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TenantResource":
        """Build a :class:`TenantResource` from :meth:`to_dict` output."""
        return cls(
            tenant_id=data["tenant_id"],
            resource_id=data["resource_id"],
            resource_type=data["resource_type"],
            content=data["content"],
            created_at=datetime.fromisoformat(data["created_at"]),
        )
