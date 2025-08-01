import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np

def create_lsp_hierarchy():
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 14)
    ax.axis('off')
    
    # Color scheme
    colors = {
        'session': '#007acc',      # Blue - top level
        'snapshot': '#00d4aa',     # Green - snapshot level
        'project': '#f39c12',      # Orange - project level
        'config': '#e74c3c',       # Red - config level
        'cache': '#9b59b6',        # Purple - cache/data
        'text': '#ffffff',         # White text
        'bg': '#1a1a1a'           # Dark background
    }
    
    fig.patch.set_facecolor(colors['bg'])
    
    # Helper function to create boxes
    def create_box(x, y, width, height, text, color, text_size=10, text_color='white'):
        box = FancyBboxPatch((x, y), width, height,
                            boxstyle="round,pad=0.1",
                            facecolor=color, edgecolor='white', linewidth=1.5)
        ax.add_patch(box)
        ax.text(x + width/2, y + height/2, text, 
                fontsize=text_size, fontweight='bold', ha='center', va='center',
                color=text_color, wrap=True)
    
    # Helper function to create connection lines
    def connect_boxes(x1, y1, x2, y2, color='white', style='-', alpha=0.7):
        ax.plot([x1, x2], [y1, y2], color=color, linewidth=2, linestyle=style, alpha=alpha)
    
    # SESSION (top level)
    create_box(2, 11.5, 12, 1.5, 'Session', colors['session'], 16)
    session_center_x = 8
    session_bottom = 11.5
    
    # Session components (level 2) - spread out more
    session_items = [
        ('Ref-counted caches\n(source file, extended tsconfigs)', 2.5),
        ('Pending changes', 1.8),
        ('File system', 1.5),
        ('Open file state', 1.8)
    ]
    
    x_positions = [2.5, 5.5, 8.5, 11.5]
    session_y = 9.5
    
    for i, ((item, width), x_pos) in enumerate(zip(session_items, x_positions)):
        create_box(x_pos, session_y, width, 1.2, item, colors['cache'], 9)
        # Connect to session with straight lines
        connect_boxes(x_pos + width/2, session_y + 1.2, session_center_x, session_bottom)
    
    # Current Snapshot (major component)
    snapshot_y = 7.5
    create_box(3, snapshot_y, 10, 1.2, 'Current Snapshot', colors['snapshot'], 14)
    snapshot_center_x = 8
    
    # Connect session to snapshot
    connect_boxes(session_center_x, session_bottom, snapshot_center_x, snapshot_y + 1.2)
    
    # Snapshot components - better positioning
    create_box(1, 5.5, 2.5, 1, 'Cached FS', colors['cache'], 10)
    create_box(4.5, 5.5, 2.5, 1, 'Open file state', colors['cache'], 10)
    create_box(8, 5.5, 3.5, 1, 'ProjectCollection', colors['project'], 11)
    create_box(12.5, 5.5, 3, 1, 'ConfigFileRegistry', colors['config'], 10)
    
    # Connect snapshot to its components
    connect_boxes(snapshot_center_x, snapshot_y, 2.25, 6.5)  # Cached FS
    connect_boxes(snapshot_center_x, snapshot_y, 5.75, 6.5)  # Open file state  
    connect_boxes(snapshot_center_x, snapshot_y, 9.75, 6.5)  # ProjectCollection
    connect_boxes(snapshot_center_x, snapshot_y, 14, 6.5)    # ConfigFileRegistry
    
    # Project details - positioned under ProjectCollection
    create_box(6, 3.5, 3, 0.8, 'File watcher registrations', colors['cache'], 9)
    create_box(6, 2.5, 3, 0.8, 'Program, LS, CheckerPool', colors['cache'], 9)
    
    # Connect ProjectCollection to its details
    connect_boxes(9.75, 5.5, 7.5, 4.3)  # File watcher registrations
    connect_boxes(9.75, 5.5, 7.5, 3.3)  # Program, LS, CheckerPool
    
    # ConfigFileRegistry details - positioned under ConfigFileRegistry
    create_box(11, 3.5, 3, 0.8, 'File watcher registrations', colors['cache'], 9)
    create_box(11, 2.5, 3, 0.8, 'ParsedCommandLine', colors['cache'], 9)
    
    # Connect ConfigFileRegistry to its details
    connect_boxes(14, 5.5, 12.5, 4.3)  # File watcher registrations
    connect_boxes(14, 5.5, 12.5, 3.3)  # ParsedCommandLine
    
    # Add hierarchy level labels
    level_labels = [
        (0.5, 12.2, 'Session'),
        (0.5, 10.1, 'Session\nComponents'),
        (0.5, 8.1, 'Snapshot'),
        (0.5, 6.0, 'Snapshot\nComponents'),
        (0.5, 3.0, 'Component\nDetails')
    ]
    
    for x, y, label in level_labels:
        ax.text(x, y, label, fontsize=9, color=colors['text'], 
                ha='center', va='center', alpha=0.8, 
                bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.5))
    
    plt.tight_layout()
    return fig

# Generate the diagram
if __name__ == "__main__":
    fig = create_lsp_hierarchy()
    fig.patch.set_facecolor('#1a1a1a')  # Dark background
    plt.savefig('presentation-diagrams/lsp-presentation/lsp-hierarchy.png', 
                dpi=300, bbox_inches='tight', facecolor='#1a1a1a')
    plt.close()
    print("Generated: lsp-hierarchy.png")
