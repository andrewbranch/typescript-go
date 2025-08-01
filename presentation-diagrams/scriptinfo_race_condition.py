import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np

def create_scriptinfo_race_condition():
    """Create a diagram showing the race condition problem with mutable ScriptInfo"""
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 9)
    ax.axis('off')
    
    # Color scheme
    colors = {
        'server': '#3498db',      # Blue for server events
        'ls': '#2ecc71',          # Green for LS events
        'scriptinfo': '#e74c3c',  # Red for ScriptInfo
        'problem': '#f39c12',     # Orange for problem
        'timeline': '#95a5a6',    # Gray for timeline
        'box': '#34495e'          # Dark gray for boxes
    }
    
    # Title
    ax.text(6, 8.5, 'Race Condition: Server vs Language Service Events', 
            fontsize=20, fontweight='bold', ha='center', color='white')
    
    # Timeline arrow
    timeline_y = 7.8
    ax.arrow(0.5, timeline_y, 11, 0, head_width=0.1, head_length=0.15, 
             fc=colors['timeline'], ec=colors['timeline'], linewidth=2)
    ax.text(6, timeline_y + 0.3, 'Time →', ha='center', fontsize=12, color='white')
    
    # Row labels
    ax.text(0.2, 6.5, 'Server\nEvents', ha='center', va='center', fontsize=12, 
            fontweight='bold', color=colors['server'], rotation=90)
    ax.text(0.2, 3.5, 'Language\nService\nEvents', ha='center', va='center', fontsize=12, 
            fontweight='bold', color=colors['ls'], rotation=90)
    
    # ScriptInfo box (center, persistent)
    scriptinfo_box = FancyBboxPatch((4.5, 1), 3, 1.2, 
                                   boxstyle="round,pad=0.1", 
                                   facecolor=colors['scriptinfo'], 
                                   edgecolor='white', linewidth=2, alpha=0.8)
    ax.add_patch(scriptinfo_box)
    ax.text(6, 1.6, 'ScriptInfo (Mutable)', ha='center', va='center', 
            fontsize=12, fontweight='bold', color='white')
    ax.text(6, 1.3, 'text: "content"\nlineMap: [0, 10, 25]', 
            ha='center', va='center', fontsize=10, color='white')
    
    # SERVER EVENTS ROW (top)
    # 1a. Hover request
    server1_box = FancyBboxPatch((1, 6), 2, 1, 
                                boxstyle="round,pad=0.1", 
                                facecolor=colors['box'], 
                                edgecolor=colors['server'], linewidth=2)
    ax.add_patch(server1_box)
    ax.text(2, 6.5, 'Hover Request\nline:2, char:5', ha='center', va='center', 
            fontsize=11, fontweight='bold', color='white')
    
    # 2a. File change (moved left)
    server2_box = FancyBboxPatch((6.5, 6), 2, 1, 
                                boxstyle="round,pad=0.1", 
                                facecolor=colors['box'], 
                                edgecolor=colors['problem'], linewidth=3)
    ax.add_patch(server2_box)
    ax.text(7.5, 6.5, 'File Change\n(concurrent)', ha='center', va='center', 
            fontsize=11, fontweight='bold', color='white')
    
    # LANGUAGE SERVICE EVENTS ROW (bottom)
    # 1b. Convert to position (moved right)
    ls1_box = FancyBboxPatch((2.5, 3), 2, 1, 
                            boxstyle="round,pad=0.1", 
                            facecolor=colors['box'], 
                            edgecolor=colors['ls'], linewidth=2)
    ax.add_patch(ls1_box)
    ax.text(3.5, 3.5, 'Convert to\nposition: 30', ha='center', va='center', 
            fontsize=11, fontweight='bold', color='white')
    
    # 2b. Compute hover
    ls2_box = FancyBboxPatch((5.5, 3), 2, 1, 
                            boxstyle="round,pad=0.1", 
                            facecolor=colors['box'], 
                            edgecolor=colors['ls'], linewidth=2)
    ax.add_patch(ls2_box)
    ax.text(6.5, 3.5, 'Compute\nHover', ha='center', va='center', 
            fontsize=11, fontweight='bold', color='white')
    
    # 3b. Convert to line/char
    ls3_box = FancyBboxPatch((8.5, 3), 2, 1, 
                            boxstyle="round,pad=0.1", 
                            facecolor=colors['box'], 
                            edgecolor=colors['ls'], linewidth=2)
    ax.add_patch(ls3_box)
    ax.text(9.5, 3.5, 'Convert to\nline:char', ha='center', va='center', 
            fontsize=11, fontweight='bold', color='white')
    
    # ARROWS
    # 1a -> 1b
    ax.arrow(2, 6, 1.5, -1.8, head_width=0.15, head_length=0.15, 
             fc=colors['server'], ec=colors['server'], linewidth=2)
    ax.text(2.8, 5, 'triggers', ha='center', fontsize=11, fontweight='bold', color='white')
    
    # 1b -> ScriptInfo
    ax.arrow(4, 3, 1, -1.5, head_width=0.15, head_length=0.15, 
             fc=colors['ls'], ec=colors['ls'], linewidth=2)
    ax.text(4.5, 2.2, 'reads', ha='center', fontsize=11, fontweight='bold', color='white')
    
    # 1b -> 2b
    ax.arrow(4.5, 3.5, 0.8, 0, head_width=0.15, head_length=0.15, 
             fc=colors['ls'], ec=colors['ls'], linewidth=2)
    
    # 2b -> 3b
    ax.arrow(7.5, 3.5, 0.8, 0, head_width=0.15, head_length=0.15, 
             fc=colors['ls'], ec=colors['ls'], linewidth=2)
    
    # 3b -> ScriptInfo (the problematic read)
    ax.arrow(9, 3, -1.5, -1.5, head_width=0.15, head_length=0.15, 
             fc=colors['problem'], ec=colors['problem'], linewidth=3)
    ax.text(8.2, 2.2, 'reads\n(WRONG!)', ha='center', fontsize=11, fontweight='bold', 
            color=colors['problem'])
    
    # 2a -> ScriptInfo (mutation) - improved text positioning
    ax.arrow(7.5, 6, -1, -4.5, head_width=0.15, head_length=0.15, 
             fc=colors['problem'], ec=colors['problem'], linewidth=3)
    ax.text(6.5, 4.8, 'MUTATES\ntext & lineMap!', ha='center', fontsize=12, 
            fontweight='bold', color='white',
            bbox=dict(boxstyle="round,pad=0.3", facecolor=colors['problem'], alpha=0.9))
    
    # Problem indicators - remove stray warning icon
    ax.text(9.5, 2.2, '💥', fontsize=24, ha='center', va='center')
    
    # Explanation
    explanation = ("File change mutates ScriptInfo between initial read and final conversion,\n"
                  "causing incorrect position mapping in the hover response!")
    ax.text(6, 0.3, explanation, ha='center', va='center', fontsize=12, 
            color=colors['problem'], fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.4", facecolor='black', alpha=0.9))
    
    plt.tight_layout()
    return fig

# Generate the diagram
if __name__ == "__main__":
    fig = create_scriptinfo_race_condition()
    fig.patch.set_facecolor('#1a1a1a')  # Dark background
    plt.savefig('presentation-diagrams/lsp-presentation/scriptinfo-race-condition.png', 
                dpi=300, bbox_inches='tight', facecolor='#1a1a1a')
    plt.close()
    print("Generated: scriptinfo-race-condition.png")
