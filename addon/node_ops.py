"""Geometry Nodes operation stubs for MCP-controlled editing."""


def add_node(node_type: str):
    """Add a node of the given type (placeholder)."""
    return {"added": node_type}


def remove_node(node_id: str):
    """Remove a node by id (placeholder)."""
    return {"removed": node_id}


def connect_nodes(output_socket: str, input_socket: str):
    """Connect two sockets (placeholder)."""
    return {"from": output_socket, "to": input_socket}


def set_node_value(node_id: str, field: str, value):
    """Set a value on a node field (placeholder)."""
    return {"node": node_id, "field": field, "value": value}

