"""Capability definitions for the Geometry Nodes MCP interface."""

from __future__ import annotations

CAPABILITIES = {
    "list_capabilities": {
        "version": 1,
        "description": "Enumerate available Geometry Nodes operations and context snapshots.",
    },
    "get_context": {
        "version": 1,
        "params": {
            "tree_scope": ["active", "selection", "full"],
            "include_values": "bool",
            "include_groups": "bool",
        },
        "description": "Return a serialized Geometry Nodes tree",
    },
    "diff_context": {
        "version": 1,
        "params": {"previous_snapshot": "object"},
        "description": "Compute a diff between snapshots",
    },
    "remove_node": {
        "version": 1,
        "params": {"node_id": "string", "dry_run": "bool"},
        "description": "Remove a node by identifier",
    },
    "connect_nodes": {
        "version": 1,
        "params": {"output_socket": "string", "input_socket": "string", "dry_run": "bool"},
        "description": "Connect two sockets if compatible",
    },
    "set_node_value": {
        "version": 1,
        "params": {"node_id": "string", "field": "string", "value": "any", "dry_run": "bool"},
        "description": "Mutate a node field value",
    },
}


def list_capabilities():
    """Return declared MCP capabilities."""

    return CAPABILITIES
