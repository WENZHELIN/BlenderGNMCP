# Blender Geometry Nodes MCP Add-on Development Plan

## Goals
- Provide a chat-driven assistant that can inspect, edit, and construct Blender Geometry Nodes networks via an MCP (Model Control Protocol) server.
- Deliver an add-on that exposes the MCP interface and keeps the AI aware of the current node-tree context, including nested node groups.
- Enable repeatable, testable workflows for geometry-node engineering that are suitable for "vibe coding" / conversational iteration.

## High-Level Features
1. **Geometry Node MCP Operations**: CRUD operations on nodes, rerouting links, setting parameters, and invoking common operators (duplicate, mute, frame, group).
2. **Context Understanding**: Structured dumps of the active node tree, selection state, and dependency hierarchy so the assistant can reason about every layer.
3. **Blender Add-on Packaging**: Self-contained add-on that registers MCP handlers, UI toggles, and background services inside Blender.

## Architecture Overview
- **MCP Server (Python)**
  - Runs inside Blender and communicates over a local transport (e.g., WebSocket/HTTP/stdio) depending on MCP spec.
  - Dispatches commands to Blender's `bpy` API and serializes responses.
  - Maintains capability discovery metadata (e.g., supported verbs, parameter schemas, rate limits).

- **Context Extractor**
  - Reads `bpy.context` to locate the active Geometry Node modifier and its node tree.
  - Traverses node groups recursively, emitting a normalized JSON structure with:
    - Node identifiers, labels, types, positions, and key properties.
    - Links (from socket to socket), including muted and rerouted connections.
    - Selection and active status for nodes and sockets.
    - Group instance boundaries with references to their source trees.
  - Provides incremental diffs to reduce payload size when only selections/values change.

- **Command Layer**
  - Maps MCP intents to concrete Blender operations (e.g., `add_node`, `connect`, `set_value`, `rename`, `align`, `frame`).
  - Applies validation against node socket types and ensures operations are scoped to the active node editor.
  - Supports dry-run/preview mode for AI planning before mutation.

- **Add-on UX Hooks**
  - Preferences panel for configuring MCP endpoint (host/port/token) and logging verbosity.
  - Status panel in the Geometry Node editor for quick enable/disable and viewing the last AI action.
  - Optional operator to trigger a context snapshot and copy it to clipboard for debugging.

## MCP Capability Sketch
- `list_capabilities`: Advertise supported node and context operations.
- `get_context`: Return current node-tree JSON with selectable depth (active selection only vs full tree).
- `apply_patch`: Batch apply node insertions, deletions, property edits, and link changes.
- `run_operator`: Invoke specific Blender operators (e.g., `node.duplicate_move`, `node.group_make`).
- `preview_patch`: Validate and simulate an `apply_patch` without committing.
- `watch_context`: Stream updates when selection or values change (throttled).

## Data Contracts (initial draft)
- **Node Representation**
  - `id`, `name`, `type`, `label`, `location`, `width`, `height`
  - `properties`: typed key/value pairs (with enums and min/max for numeric values)
  - `inputs`/`outputs`: sockets with `id`, `name`, `data_type`, `default_value`, `links`
- **Link Representation**
  - `from_node`, `from_socket`, `to_node`, `to_socket`, `is_muted`, `is_reroute`
- **Context Payload**
  - `tree_name`, `object`, `modifier`, `active_frame`, `selected_nodes`, `active_node`, `groups`

## Development Steps
1. **Bootstrap Add-on**
   - Create `__init__.py` with add-on metadata and registration hooks.
   - Add a lightweight logging utility and preference storage for endpoint/token.

2. **Transport & Server**
   - Implement an MCP transport abstraction (start with stdio or localhost WebSocket).
   - Add request router with JSON schema validation for each command.

3. **Context Extraction**
   - Build recursive traversal utilities for node trees and node groups.
   - Implement diffing for selections and property changes.

4. **Command Execution**
   - Implement node creation (`bpy.types.GeometryNodeTree.nodes.new`), linking, deletion, and property setters with type checks.
   - Add undo-safe wrappers to group changes and expose dry-run mode.

5. **UI/UX Layer**
   - Preferences for endpoint configuration, auth token, and logging level.
   - Panel in the Geometry Nodes editor showing connection status and quick actions.

6. **Testing & CI**
   - Add headless Blender test harness for executing scripted MCP sessions.
   - Validate serialization for a sample node tree (e.g., distribute points -> instance -> realize).

## Security & Safety Considerations
- Require optional API token for inbound MCP connections.
- Constrain operations to the active Blender session; reject file I/O or Python execution requests.
- Provide rate limiting on streaming context updates to avoid UI stalls.

## Tooling & Dependencies
- **Runtime**: Blender 4.x with Python 3.11+ bundled interpreter.
- **Libraries**: Standard library (`asyncio`, `json`, `dataclasses`) and Blender `bpy` API.
- **Dev Tools**: `pytest` for unit tests, `ruff` for style if permitted by Blender environment.

## Open Questions
- Which MCP transport is preferred (stdio vs WebSocket) for the target orchestration stack?
- Should the add-on expose a minimal UI, or rely solely on MCP for headless operation?
- How granular should `get_context` be (full tree vs active group vs selection-only)?
