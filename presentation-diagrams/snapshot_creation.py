import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

def create_snapshot_creation():
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Color scheme
    colors = {
        'input': '#9b59b6',        # Purple - inputs
        'process': '#f39c12',      # Orange - intermediate results
        'snapshot': '#00d4aa',     # Green - snapshots
        'output': '#27ae60',       # Darker green - final output
        'container': '#34495e',    # Dark gray - container
        'text': '#ffffff',         # White text
        'bg': '#1a1a1a'           # Dark background
    }
    
    fig.patch.set_facecolor(colors['bg'])
    
    # Helper function to create boxes
    def create_box(x, y, width, height, text, color, text_size=14, text_color='white', alpha=1.0):
        box = FancyBboxPatch((x, y), width, height,
                            boxstyle="round,pad=0.1",
                            facecolor=color, edgecolor='white', linewidth=1.5, alpha=alpha)
        ax.add_patch(box)
        ax.text(x + width/2, y + height/2, text, 
                fontsize=text_size, fontweight='bold', ha='center', va='center',
                color=text_color, wrap=True)
        return (x + width/2, y + height/2)  # Return center point
    
    # Helper function to create arrows
    def create_arrow(x1, y1, x2, y2, color='white'):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                   arrowprops=dict(arrowstyle='->', color=color, lw=3))
    
    # STEP 1: Initial inputs
    step1_y = 7
    
    # Initial inputs
    pending_center = create_box(1, step1_y, 2.5, 1, 'Pending\nChanges', colors['input'], 14)
    overlay_center = create_box(1, step1_y - 1.5, 2.5, 1, 'Overlay\nState', colors['input'], 14)
    
    # Container for step 1 outputs
    container_center = create_box(5, step1_y - 1, 3.5, 2.5, '', colors['container'], 10, alpha=0.3)
    
    # Step 1 outputs inside container
    new_overlay_center = create_box(5.25, step1_y, 3, 0.8, 'New Overlay State', colors['process'], 12)
    file_summary_center = create_box(5.25, step1_y - 1.2, 3, 0.8, 'FileChangeSummary', colors['process'], 12)
    
    # STEP 2: Additional inputs (moved left, underneath step 1 outputs)
    step2_y = 4
    
    # Additional inputs - moved left to be underneath "New Overlay State" and "FileChangeSummary"
    current_snap_center = create_box(5.25, step2_y, 3, 1, 'Current\nSnapshot', colors['snapshot'], 14)
    ref_cache_center = create_box(5.25, step2_y - 1.5, 3, 1, 'Ref-counted\nCaches', colors['input'], 14)
    
    # Final output - moved left
    final_center = create_box(9.5, 3.25, 2.5, 1.5, 'New Snapshot', colors['output'], 15)
    
    # ARROWS
    
    # Step 1: Inputs converge to container center
    create_arrow(pending_center[0] + 1.25, pending_center[1], 
                container_center[0] - 1.75, container_center[1] + 0.5, 
                colors['process'])
    
    create_arrow(overlay_center[0] + 1.25, overlay_center[1], 
                container_center[0] - 1.75, container_center[1] - 0.5, 
                colors['process'])
    
    # Container to final output - updated for shorter distance
    create_arrow(container_center[0] + 1.75, container_center[1], 
                final_center[0] - 1.25, final_center[1], 
                colors['process'])
    
    # Step 2: Additional inputs to final result - updated for shorter distance
    create_arrow(current_snap_center[0] + 1.5, current_snap_center[1], 
                final_center[0] - 1.25, final_center[1] + 0.3, 
                colors['snapshot'])
    
    create_arrow(ref_cache_center[0] + 1.5, ref_cache_center[1], 
                final_center[0] - 1.25, final_center[1] - 0.3, 
                colors['input'])
    
    # Add step labels
    ax.text(2.25, 8.5, 'Step 1: Process Changes', fontsize=12, ha='center', va='center',
           color=colors['text'], fontweight='bold',
           bbox=dict(boxstyle="round,pad=0.4", facecolor=colors['process'], alpha=0.3))
    
    ax.text(6.75, 5.5, 'Step 2: Combine Resources', fontsize=12, ha='center', va='center',
           color=colors['text'], fontweight='bold',
           bbox=dict(boxstyle="round,pad=0.4", facecolor=colors['snapshot'], alpha=0.3))
    
    # Add explanatory text - centered for smaller canvas
    ax.text(6, 1, 'All inputs combine to create an immutable snapshot\nwith updated file states and cached resources', 
           fontsize=10, ha='center', va='center',
           color=colors['text'], alpha=0.8, style='italic')
    
    plt.tight_layout()
    return fig

# Generate the diagram
if __name__ == "__main__":
    fig = create_snapshot_creation()
    fig.patch.set_facecolor('#1a1a1a')  # Dark background
    plt.savefig('lsp-presentation/snapshot-creation.png', 
                dpi=300, bbox_inches='tight', facecolor='#1a1a1a')
    plt.close()
    print("Generated: snapshot-creation.png")
