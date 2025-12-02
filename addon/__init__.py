"""Blender Geometry Nodes MCP add-on entrypoint."""

from __future__ import annotations

import importlib.util
import logging
from typing import Optional

from .mcp_server import MCPServer

_LOGGER = logging.getLogger(__name__)
_LOGGER.addHandler(logging.NullHandler())

_BPY_SPEC = importlib.util.find_spec("bpy")
if _BPY_SPEC:
    import bpy
else:
    bpy = None

_server: Optional[MCPServer] = None


DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_TRANSPORT = "stdio"


def configure_logging(level: str = DEFAULT_LOG_LEVEL) -> None:
    """Configure base logging for the add-on.

    The default targets Blender's console. File logging can be added later via
    preferences without affecting MCP behavior.
    """

    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(level=numeric_level, format="[GeometryNodesMCP] %(levelname)s: %(message)s")
    _LOGGER.debug("Logging configured to level %s", level)


if bpy:

    class GeometryNodesMCPPreferences(bpy.types.AddonPreferences):
        """User-configurable settings for the MCP add-on."""

        bl_idname = __package__ or __name__

        transport_mode: bpy.props.EnumProperty(
            name="Transport",
            description="MCP transport channel",
            items=[
                ("stdio", "Stdio", "Run MCP over stdio inside Blender"),
                ("websocket", "WebSocket", "Serve MCP over an authenticated local WebSocket"),
            ],
            default=DEFAULT_TRANSPORT,
        )

        log_level: bpy.props.EnumProperty(
            name="Log level",
            description="Verbosity for MCP operations",
            items=[(lvl, lvl.title(), f"Set log level to {lvl}") for lvl in ("DEBUG", "INFO", "WARNING", "ERROR")],
            default=DEFAULT_LOG_LEVEL,
        )

        enable_file_logging: bpy.props.BoolProperty(
            name="File logging",
            description="Write MCP events to a rotating log file in the temp directory",
            default=False,
        )

        def draw(self, context):  # type: ignore[override]
            layout = self.layout
            layout.label(text="Geometry Nodes MCP")
            layout.prop(self, "transport_mode")
            layout.prop(self, "log_level")
            layout.prop(self, "enable_file_logging")

else:

    class GeometryNodesMCPPreferences:  # type: ignore[too-few-public-methods]
        """Fallback stub when bpy is unavailable (e.g., unit tests)."""

        bl_idname = __name__
        transport_mode: str = DEFAULT_TRANSPORT
        log_level: str = DEFAULT_LOG_LEVEL
        enable_file_logging: bool = False

        def draw(self, context):
            raise RuntimeError("Preferences UI is only available inside Blender")


def get_preferences(context=None) -> GeometryNodesMCPPreferences:
    """Return add-on preferences or defaults when Blender isn't available."""

    if bpy and context:
        return context.preferences.addons[__package__].preferences  # type: ignore[index]
    return GeometryNodesMCPPreferences()


def register():
    """Register the add-on with Blender."""

    global _server
    if not bpy:
        raise RuntimeError("This add-on must run inside Blender to register")

    configure_logging(get_preferences().log_level)
    bpy.utils.register_class(GeometryNodesMCPPreferences)

    _server = MCPServer(transport=get_preferences().transport_mode)
    _server.start()
    _LOGGER.info("Geometry Nodes MCP add-on registered with %s transport", _server.transport)


def unregister():
    """Unregister the add-on from Blender."""

    global _server
    if not bpy:
        return

    if _server:
        _server.stop()
        _LOGGER.info("Geometry Nodes MCP server stopped")
        _server = None

    bpy.utils.unregister_class(GeometryNodesMCPPreferences)
    _LOGGER.info("Geometry Nodes MCP add-on unregistered")
