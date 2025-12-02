# MCP Interface for Blender Geometry Nodes

This document outlines the MCP-facing behaviors needed for conversational control of Geometry Nodes. It focuses on capability definitions, context payloads, and lifecycle considerations for the add-on implementation.

## Capability Definitions
- **`list_capabilities`**: Enumerate supported verbs, schema versions, and experimental flags.
- **`get_context`**
  - Inputs: `tree_scope` (`active`, `selection`, `full`), `include_values` (bool), `include_groups` (bool).
  - Output: Serialized node tree JSON with IDs, sockets, links, selection state, and optional per-socket default values.
- **`apply_patch`**
  - Supports batch mutations: create/delete nodes, edit properties, create/remove links, rename, set labels, toggle mute, and reroute creation.
  - Accepts `atomic` flag to wrap changes in a single undo step.
- **`preview_patch`**: Validates `apply_patch` payloads without committing; returns rejected operations with reasons.
- **`run_operator`**: Executes Blender operators that are hard to model as patches (e.g., `node.group_make`, `node.translate_attach`).
- **`watch_context`**: Streams diffs when selection or values change; includes throttling and debounce controls.

## Context Serialization Rules
- Each node gets a stable `id` combining `tree_name` and Blender `Node.name` to survive label edits.
- Socket entries include `data_type`, `default_value` (when serializable), and `linked` status.
- Links reference sockets by node ID and socket index; reroute nodes are first-class to preserve layout.
- Group instances include `source_tree` reference and instance-level overrides if present.
- Include `frame` references to support layout-aware operations.

## Geometry-Node-Specific Operations
- Create standard node templates (e.g., Distribute Points on Faces → Instance on Points → Realize Instances pipeline).
- Manage named attributes on geometry sockets, including field status and data type validation.
- Handle simulation and repeat zones with entry/exit node pairing awareness.

## Error Handling & Safety
- Reject patches when target trees are not Geometry Node trees or modifier is missing.
- Validate socket compatibility before linking; return actionable errors for type mismatches.
- Provide dry-run warnings for operations that would remove linked data (e.g., deleting nodes with multi-links).

## Testing Strategy
- Scripted MCP sessions that:
  1. Request context of a sample Geometry Node setup.
  2. Add a reroute node and reconnect links.
  3. Insert a Group node, open the group, and modify an internal node parameter.
  4. Delete a node and confirm link cleanup via `get_context`.
- CI should run these sessions headlessly in Blender and assert JSON snapshots.

## Add-on Packaging Notes
- Register a background task for the MCP transport; ensure it stops on `register`/`unregister` lifecycle events.
- Expose a Preferences section for endpoint/token and a panel in the Geometry Node editor for status.
- Ship default logging to Blender's console and an optional rotating file handler for longer sessions.
