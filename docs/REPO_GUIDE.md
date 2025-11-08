# Repository Guide

This guide outlines conventions for the Dofus bot monorepo.

## Structure
- `core/`: Rust components
- `orchestrator/`: Python coordination
- `ui/`: Electron/Svelte interface
- `docs/`: Documentation, including diagrams in `docs/diagrams/`

## Adding Diagrams
Place new PlantUML diagrams in `docs/diagrams/` with .puml extension. Generate SVGs using PlantUML and update `docs/diagrams/README.md` with descriptions.