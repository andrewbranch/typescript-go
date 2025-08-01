# Presentation Diagrams

This folder contains Python scripts for generating diagrams for the LSP server presentation.

## Available Libraries

- **matplotlib** - Basic plots and charts
- **diagrams** - Architecture diagrams with icons
- **graphviz** - Directed graphs and flowcharts
- **networkx** - Network/graph visualizations
- **plotly** - Interactive diagrams
- **seaborn** - Statistical visualizations

## Usage

Run Python scripts with:
```bash
/Users/andrew/Developer/microsoft/typescript-go/.venv/bin/python script_name.py
```

## Current Diagrams

### dirty.Map Visualization
- `dirty_map_diagrams.py` - Generates diagrams explaining the dirty.Map pattern
- Output folder: `dirty-map/`
  - `dirty_map_clean_state.png` - Clean state with no pending changes
  - `dirty_map_with_changes.png` - State with pending changes showing cloning
  - `dirty_map_finalization.png` - Finalization process creating new immutable map
