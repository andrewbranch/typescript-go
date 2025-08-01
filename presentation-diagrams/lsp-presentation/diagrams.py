import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np

def create_scriptinfo_race_condition():
    """Create a diagram showing the race condition problem with mutable ScriptInfo"""
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Color scheme
    colors = {
        'client': '#3498db',      # Blue
        'server': '#2ecc71',      # Green  
        'scriptinfo': '#e74c3c',  # Red
        'problem': '#f39c12',     # Orange
        'timeline': '#95a5a6'     # Gray
    }
    
    # Title
    ax.text(5, 7.5, 'Race Condition Problem: Mutable ScriptInfo', 
            fontsize=20, fontweight='bold', ha='center',
            color='white')
    
    # Timeline
    timeline_y = 6.5
    ax.arrow(0.5, timeline_y, 9, 0, head_width=0.1, head_length=0.1, 
             fc=colors['timeline'], ec=colors['timeline'], linewidth=2)
    ax.text(5, timeline_y + 0.3, 'Time →', ha='center', fontsize=12, color='white')
    
    # ScriptInfo box (center, persistent)
    scriptinfo_box = FancyBboxPatch((3.5, 4), 3, 1.5, 
                                   boxstyle="round,pad=0.1", 
                                   facecolor=colors['scriptinfo'], 
                                   edgecolor='white', linewidth=2, alpha=0.8)
    ax.add_patch(scriptinfo_box)
    ax.text(5, 4.75, 'ScriptInfo\n(Mutable)', ha='center', va='center', 
            fontsize=12, fontweight='bold', color='white')
    ax.text(5, 4.25, 'text: "old content"\nlineMap: [0, 10, 25]', 
            ha='center', va='center', fontsize=10, color='white')
    
    # Step 1: LSP Request comes in
    step1_box = FancyBboxPatch((0.5, 2.5), 2, 1, 
                              boxstyle="round,pad=0.1", 
                              facecolor=colors['client'], 
                              edgecolor='white', linewidth=2, alpha=0.8)
    ax.add_patch(step1_box)
    ax.text(1.5, 3, '1. LSP Request\nline:2, char:5', ha='center', va='center', 
            fontsize=10, fontweight='bold', color='white')
    
    # Arrow from request to scriptinfo
    ax.arrow(2.5, 3, 1, 1, head_width=0.1, head_length=0.1, 
             fc=colors['client'], ec=colors['client'], linewidth=2)
    ax.text(3, 3.7, 'Convert to\nposition: 30', ha='center', fontsize=9, 
            color='white', bbox=dict(boxstyle="round,pad=0.2", facecolor=colors['client'], alpha=0.7))
    
    # Step 2: File change request (concurrent)
    step2_box = FancyBboxPatch((7.5, 2.5), 2, 1, 
                              boxstyle="round,pad=0.1", 
                              facecolor=colors['problem'], 
                              edgecolor='white', linewidth=2, alpha=0.8)
    ax.add_patch(step2_box)
    ax.text(8.5, 3, '2. File Change\n(concurrent)', ha='center', va='center', 
            fontsize=10, fontweight='bold', color='white')
    
    # Arrow from file change to scriptinfo
    ax.arrow(7.5, 3, -1, 1, head_width=0.1, head_length=0.1, 
             fc=colors['problem'], ec=colors['problem'], linewidth=2)
    ax.text(7, 3.7, 'Mutates text\n& lineMap!', ha='center', fontsize=9, 
            color='white', bbox=dict(boxstyle="round,pad=0.2", facecolor=colors['problem'], alpha=0.7))
    
    # Step 3: LS operation completes
    step3_box = FancyBboxPatch((0.5, 0.5), 2, 1, 
                              boxstyle="round,pad=0.1", 
                              facecolor=colors['server'], 
                              edgecolor='white', linewidth=2, alpha=0.8)
    ax.add_patch(step3_box)
    ax.text(1.5, 1, '3. LS Result\nposition: 45', ha='center', va='center', 
            fontsize=10, fontweight='bold', color='white')
    
    # Arrow from LS back to scriptinfo (for conversion back)
    ax.arrow(2.5, 1, 1, 2.5, head_width=0.1, head_length=0.1, 
             fc=colors['server'], ec=colors['server'], linewidth=2)
    ax.text(3, 2, 'Convert back\nto line:char', ha='center', fontsize=9, 
            color='white', bbox=dict(boxstyle="round,pad=0.2", facecolor=colors['server'], alpha=0.7))
    
    # Problem indicator
    problem_box = FancyBboxPatch((7.5, 0.5), 2, 1, 
                                boxstyle="round,pad=0.1", 
                                facecolor=colors['problem'], 
                                edgecolor='white', linewidth=2, alpha=0.8)
    ax.add_patch(problem_box)
    ax.text(8.5, 1, '❌ WRONG!\nInconsistent\nlineMap used', ha='center', va='center', 
            fontsize=10, fontweight='bold', color='white')
    
    # Add warning symbols
    ax.text(5, 3.5, '⚠️', fontsize=20, ha='center', va='center')
    ax.text(5, 1.5, '💥', fontsize=20, ha='center', va='center')
    
    # Add explanation text
    explanation = ("The ScriptInfo's text and lineMap change between the initial conversion\n"
                  "and the final result conversion, causing incorrect position mapping!")
    ax.text(5, 0.2, explanation, ha='center', va='center', fontsize=12, 
            color=colors['problem'], fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.8))
    
    plt.tight_layout()
    return fig

# Generate the diagram
if __name__ == "__main__":
    fig = create_scriptinfo_race_condition()
    fig.patch.set_facecolor('#1a1a1a')  # Dark background
    plt.savefig('/Users/andrew/Developer/microsoft/typescript-go/presentation-diagrams/lsp-presentation/scriptinfo-race-condition.png', 
                dpi=300, bbox_inches='tight', facecolor='#1a1a1a')
    plt.close()
    print("Generated: scriptinfo-race-condition.png")
