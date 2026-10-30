"""Nexent — tenant resource management & retrieval (skeleton stage).

This package follows the layout conventions of the upstream open-source
project ModelEngine-Group/nexent (``sdk/nexent`` flat package with domain
sub-packages) without copying any of its code.

Public entry point for this stage: :mod:`nexent.resources` — the tenant
resource management & retrieval module.
"""

__version__ = "0.1.0"

from nexent.resources import ResourceRepository, TenantResource

__all__ = ["ResourceRepository", "TenantResource", "__version__"]
