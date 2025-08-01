import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

def create_snapshot_creation():
    fig, ax = plt.subplots(1, 1, figsize=(16, 8))
    ax.set_xlim(0, 16)
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
    def create_box(x, y, width, height, text, color, text_size=10, text_color='white', alpha=1.0):
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
    pending_center = create_box(1, step1_y, 2.5, 1, 'Pending\nChanges', colors['input'], 10)
    overlay_center = create_box(1, step1_y - 1.5, 2.5, 1, 'Overlay\nState', colors['input'], 10)
    
    # Container for step 1 outputs
    container_center = create_box(5, step1_y - 1, 3.5, 2.5, '', colors['container'], 10, alpha=0.3)
    
    # Step 1 outputs inside container
    new_overlay_center = create_box(5.25, step1_y, 3, 0.8, 'New Overlay State', colors['process'], 9)
    file_summary_center = create_box(5.25, step1_y - 1.2, 3, 0.8, 'FileChangeSummary', colors['process'], 9)
    
    # STEP 2: Additional inputs (moved right)
    step2_y = 4
    
    # Additional inputs
    current_snap_center = create_box(10, step2_y, 2.5, 1, 'Current\nSnapshot', colors['snapshot'], 10)
    ref_cache_center = create_box(10, step2_y - 1.5, 2.5, 1, 'Ref-counted\nCaches', colors['input'], 10)
    
    # Final output
    final_center = create_box(13.5, 3.25, 2.5, 1.5, 'New Snapshot', colors['output'], 11)
    
    # ARROWS
    
    # Step 1: Inputs converge to container center
    create_arrow(pending_center[0] + 1.25, pending_center[1], 
                container_center[0] - 1.75, container_center[1] + 0.5, 
                colors['process'])
    
    create_arrow(overlay_center[0] + 1.25, overlay_center[1], 
                container_center[0] - 1.75, container_center[1] - 0.5, 
                colors['process'])
    
    # Container to final output
    create_arrow(container_center[0] + 1.75, container_center[1], 
                final_center[0] - 1.25, final_center[1], 
                colors['process'])
    
    # Step 2: Additional inputs to final result
    create_arrow(current_snap_center[0] + 1.25, current_snap_center[1], 
                final_center[0] - 1.25, final_center[1] + 0.3, 
                colors['snapshot'])
    
    create_arrow(ref_cache_center[0] + 1.25, ref_cache_center[1], 
                final_center[0] - 1.25, final_center[1] - 0.3, 
                colors['input'])
    
    # Add step labels
    ax.text(2.25, 8.5, 'Step 1: Process Changes', fontsize=12, ha='center', va='center',
           color=colors['text'], fontweight='bold',
           bbox=dict(boxstyle="round,pad=0.4", facecolor=colors['process'], alpha=0.3))
    
    ax.text(11.25, 5.5, 'Step 2: Combine Resources', fontsize=12, ha='center', va='center',
           color=colors['text'], fontweight='bold',
           bbox=dict(boxstyle="round,pad=0.4", facecolor=colors['snapshot'], alpha=0.3))
    
    # Add explanatory text
    ax.text(8, 1, 'All inputs combine to create an immutable snapshot\nwith updated file states and cached resources', 
           fontsize=10, ha='center', va='center',
           color=colors['text'], alpha=0.8, style='italic')
    
    plt.tight_layout()
    return fig

# Generate the diagram
if __name__ == "__main__":
    fig = create_snapshot_creation()
    fig.patch.set_facecolor('#1a1a1a')  # Dark background
    plt.savefig('presentation-diagrams/lsp-presentation/snapshot-creation.png', 
                dpi=300, bbox_inches='tight', facecolor='#1a1a1a')
    plt.close()
    print("Generated: snapshot-creation.png")
