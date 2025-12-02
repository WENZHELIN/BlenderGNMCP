"""Capability definitions for the Geometry Nodes MCP interface."""

CAPABILITIES = {
    "list_capabilities": {
        "version": 1,
        "description": "Enumerate available Geometry Nodes operations and context snapshots.",
    }
}


def list_capabilities():
    """Return declared MCP capabilities (placeholder)."""
    return CAPABILITIES

