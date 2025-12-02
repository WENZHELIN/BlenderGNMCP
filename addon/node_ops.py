"""Geometry Nodes operation stubs for MCP-controlled editing."""

from __future__ import annotations

import importlib.util
import logging
from typing import Any, Dict

_LOGGER = logging.getLogger(__name__)
_LOGGER.addHandler(logging.NullHandler())

_BPY_SPEC = importlib.util.find_spec("bpy")
if _BPY_SPEC:
    import bpy
else:
    bpy = None


def _require_bpy(operation: str) -> None:
    if not bpy:
        raise RuntimeError(f"Operation '{operation}' requires Blender runtime")


def _ensure_node_id(node_id: str) -> str:
    if not node_id:
        raise ValueError("node_id must be provided")
    return node_id


def add_node(node_type: str, dry_run: bool = False) -> Dict[str, Any]:
    """Add a node of the given type."""

    if not node_type:
        raise ValueError("node_type must be provided")

    if dry_run:
        return {"planned": True, "node_type": node_type}

    _require_bpy("add_node")
    tree = bpy.context.space_data.edit_tree
    new_node = tree.nodes.new(node_type)
    _LOGGER.info("Added node %s", new_node.name)
    return {"added": new_node.name, "type": node_type}


def remove_node(node_id: str, dry_run: bool = False) -> Dict[str, Any]:
    """Remove a node by id."""

    node_id = _ensure_node_id(node_id)

    if dry_run:
        return {"planned": True, "removed": node_id}

    _require_bpy("remove_node")
    tree = bpy.context.space_data.edit_tree
    node = tree.nodes.get(node_id)
    if not node:
        raise ValueError(f"Node '{node_id}' not found")

    tree.nodes.remove(node)
    _LOGGER.info("Removed node %s", node_id)
    return {"removed": node_id}


def connect_nodes(output_socket: str, input_socket: str, dry_run: bool = False) -> Dict[str, Any]:
    """Connect two sockets."""

    if not output_socket or not input_socket:
        raise ValueError("output_socket and input_socket are required")

    if dry_run:
        return {"planned": True, "from": output_socket, "to": input_socket}

    _require_bpy("connect_nodes")
    tree = bpy.context.space_data.edit_tree

    def _resolve(socket_path: str):
        node_name, socket_name = socket_path.split(":", 1)
        node = tree.nodes.get(node_name)
        if not node:
            raise ValueError(f"Node '{node_name}' not found")
        socket = node.outputs.get(socket_name) or node.inputs.get(socket_name)
        if not socket:
            raise ValueError(f"Socket '{socket_name}' not found on node '{node_name}'")
        return node, socket

    from_node, from_socket = _resolve(output_socket)
    to_node, to_socket = _resolve(input_socket)
    if not to_socket.is_linked or to_socket.is_multi_input:
        tree.links.new(from_socket, to_socket)
    else:
        raise ValueError(f"Socket '{input_socket}' is already linked and not multi-input")

    _LOGGER.info("Connected %s -> %s", output_socket, input_socket)
    return {"from": output_socket, "to": input_socket}


def set_node_value(node_id: str, field: str, value: Any, dry_run: bool = False) -> Dict[str, Any]:
    """Set a value on a node field."""

    node_id = _ensure_node_id(node_id)
    if not field:
        raise ValueError("field must be provided")

    if dry_run:
        return {"planned": True, "node": node_id, "field": field, "value": value}

    _require_bpy("set_node_value")
    tree = bpy.context.space_data.edit_tree
    node = tree.nodes.get(node_id)
    if not node:
        raise ValueError(f"Node '{node_id}' not found")

    if not hasattr(node, field):
        raise ValueError(f"Field '{field}' not found on node '{node_id}'")

    setattr(node, field, value)
    _LOGGER.info("Set %s.%s to %s", node_id, field, value)
    return {"node": node_id, "field": field, "value": value}
