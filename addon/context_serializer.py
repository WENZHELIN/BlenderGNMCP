"""Context serialization helpers for Geometry Nodes MCP."""

from __future__ import annotations

import importlib.util
import logging
from typing import Any, Dict, List, Optional

_LOGGER = logging.getLogger(__name__)
_LOGGER.addHandler(logging.NullHandler())

_BPY_SPEC = importlib.util.find_spec("bpy")
if _BPY_SPEC:
    import bpy
else:
    bpy = None


def _node_to_dict(node) -> Dict[str, Any]:
    return {
        "id": node.name,
        "type": node.bl_idname,
        "label": node.label,
        "mute": getattr(node, "mute", False),
        "location": list(node.location) if hasattr(node, "location") else [0, 0],
    }


def _links_to_dict(links) -> List[Dict[str, Any]]:
    link_entries: List[Dict[str, Any]] = []
    for link in links:
        link_entries.append(
            {
                "from_node": link.from_node.name,
                "from_socket": link.from_socket.name,
                "to_node": link.to_node.name,
                "to_socket": link.to_socket.name,
            }
        )
    return link_entries


def _active_tree(tree_scope: str):
    if not bpy:
        return None

    space = bpy.context.space_data
    if not space or space.type != "NODE_EDITOR":
        return None

    if tree_scope == "selection" and bpy.context.selected_nodes:
        return space.edit_tree
    return space.edit_tree


def snapshot_context(
    tree_scope: str = "active",
    include_values: bool = False,
    include_groups: bool = True,
) -> Dict[str, Any]:
    """Capture the current Geometry Nodes context."""

    tree = _active_tree(tree_scope)
    if not tree:
        return {
            "status": "unavailable",
            "reason": "No active Geometry Nodes tree or not running inside Blender",
            "tree_scope": tree_scope,
        }

    nodes = [_node_to_dict(node) for node in tree.nodes]
    links = _links_to_dict(tree.links)

    snapshot: Dict[str, Any] = {
        "status": "ok",
        "tree": tree.name,
        "nodes": nodes,
        "links": links,
        "include_values": include_values,
        "include_groups": include_groups,
    }

    _LOGGER.debug("Serialized %d nodes and %d links", len(nodes), len(links))
    return snapshot


def diff_context(previous_snapshot: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
    """Compute a diff against a previous snapshot."""

    current = snapshot_context(**kwargs)
    if not previous_snapshot or previous_snapshot.get("status") != "ok" or current.get("status") != "ok":
        return {"previous": previous_snapshot, "current": current}

    prev_nodes = {node["id"]: node for node in previous_snapshot.get("nodes", [])}
    curr_nodes = {node["id"]: node for node in current.get("nodes", [])}

    added = [node for node_id, node in curr_nodes.items() if node_id not in prev_nodes]
    removed = [node for node_id, node in prev_nodes.items() if node_id not in curr_nodes]

    changed: List[Dict[str, Any]] = []
    for node_id, node in curr_nodes.items():
        if node_id in prev_nodes and node != prev_nodes[node_id]:
            changed.append({"id": node_id, "previous": prev_nodes[node_id], "current": node})

    return {
        "status": "ok",
        "added": added,
        "removed": removed,
        "changed": changed,
        "tree": current.get("tree"),
    }
