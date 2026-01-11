# BlenderGNMCP

MCP server and Blender add-on skeleton for Geometry Nodes automation.

## Prerequisites
- Blender 4.0 or newer (API compatible with Geometry Nodes).
- Python bundled with Blender (used automatically by the add-on; no separate installation required).
- Optional: a Model Context Protocol (MCP) client such as Claude Desktop or a local MCP testing harness for driving the add-on via stdio.

## Installation
1. Download or clone this repository.
2. Create a zip of the `addon/` directory (e.g., `zip -r geometry_nodes_mcp.zip addon`). The archive will include the `blender_manifest.toml` required by Blender 4.2+ along with the add-on package.
3. In Blender, open **Edit → Preferences → Add-ons → Install…** and select the generated zip.
4. Enable **Geometry Nodes MCP** in the add-on list. The add-on will start its MCP server using the configured transport (stdio by default).

## Usage
- Configure the add-on under **Edit → Preferences → Add-ons → Geometry Nodes MCP**:
  - **Transport**: `stdio` (default) or `websocket` (stubbed for future use).
  - **Log level** and **File logging**: tune verbosity and enable rotating file logs when needed.
- Connect an MCP-aware client to the running Blender session (stdio transport is typically auto-detected by local clients when Blender is launched from a terminal).
- Use the client's chat or command interface to invoke MCP capabilities:
  - **Context inspection**: request serialized Geometry Nodes context (active object, modifier, and selected node information).
  - **Node operations**: dry-run or apply add/remove/update actions on nodes with validation.
- For development or headless validation, run Blender from a terminal to see log output emitted by the add-on.

## Development
- The add-on code lives in `addon/` with modules for capabilities, context serialization, node operations, and the MCP server router.
- Documentation, planning notes, and the evolving task list are in `docs/`.
- Example flows and helper scripts are scaffolded under `examples/` and `scripts/`.
- Tests are stubbed in `addon/tests/` and can be expanded using Blender's bundled Python for integration checks.

## Structure
- `docs/` — planning, design docs, and task list.
- `addon/` — Blender add-on package and MCP server stubs.
- `scripts/` — headless or helper scripts for MCP flows.
- `examples/` — usage transcripts and Geometry Nodes templates.
- `tools/` — developer tooling and packaging helpers.
