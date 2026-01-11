"""MCP server entry for Blender Geometry Nodes."""

from __future__ import annotations

import logging
from typing import Any, Callable, Dict

from . import capabilities
from .context_serializer import diff_context, snapshot_context
from .node_ops import connect_nodes, remove_node, set_node_value

_LOGGER = logging.getLogger(__name__)
_LOGGER.addHandler(logging.NullHandler())

Handler = Callable[[Dict[str, Any]], Dict[str, Any]]


class MCPServer:
    """Minimal MCP router with pluggable transport."""

    def __init__(self, transport: str = "stdio") -> None:
        self.transport = self._resolve_transport(transport)
        self._running = False
        self._handlers: Dict[str, Handler] = {
            "list_capabilities": lambda payload: {"capabilities": capabilities.list_capabilities()},
            "get_context": lambda payload: snapshot_context(**payload),
            "diff_context": lambda payload: diff_context(**payload),
            "remove_node": lambda payload: remove_node(**payload),
            "connect_nodes": lambda payload: connect_nodes(**payload),
            "set_node_value": lambda payload: set_node_value(**payload),
        }

    @staticmethod
    def _resolve_transport(mode: str) -> str:
        if mode not in {"stdio", "websocket"}:
            raise ValueError(f"Unsupported transport '{mode}'")
        return mode

    def start(self) -> None:
        """Start the MCP server (transport bootstrap deferred)."""

        self._running = True
        _LOGGER.info("MCP server flagged as running using %s", self.transport)

    def stop(self) -> None:
        """Stop the MCP server and clean up resources (placeholder)."""

        if not self._running:
            return
        self._running = False
        _LOGGER.info("MCP server stopped")

    def handle_request(self, method: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatch a request to the registered handler map."""

        if method not in self._handlers:
            return {"ok": False, "error": f"Unknown method '{method}'"}

        _LOGGER.debug("Handling MCP method %s with payload %s", method, payload)
        try:
            result = self._handlers[method](payload)
            return {"ok": True, "result": result}
        except Exception as exc:  # noqa: BLE001
            _LOGGER.exception("Handler for %s failed", method)
            return {"ok": False, "error": str(exc)}
