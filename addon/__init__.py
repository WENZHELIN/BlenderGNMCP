"""Blender Geometry Nodes MCP add-on entrypoint.

Provides registration hooks and shared preferences stubs for the MCP server
integration. Implementation will evolve as MCP capabilities and UI features
are added.
"""

bl_info = {
    "name": "Geometry Nodes MCP",
    "author": "OpenAI",
    "version": (0, 0, 1),
    "blender": (3, 6, 0),
    "location": "Geometry Nodes Editor",
    "description": "Chat-driven MCP interface for Geometry Nodes",
    "category": "Node",
}


def register():
    """Register the add-on with Blender.

    This placeholder will later register operators, panels, preferences, and
    initialize the MCP server lifecycle.
    """


def unregister():
    """Unregister the add-on from Blender."""

