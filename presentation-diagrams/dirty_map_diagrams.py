#!/usr/bin/env python3
"""
dirty.Map visualization for typescript-go presentation
Shows the concept of tracking pending changes to immutable base maps
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch
import matplotlib.patheffects as path_effects

# Set up the matplotlib style
plt.style.use('default')
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'sans-serif'

def create_dirty_map_clean_state():
    """Create a diagram showing dirty.Map with no pending changes"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    
    # Color scheme matching other diagrams
    colors = {
        'base': '#9b59b6',        # Purple - base/immutable data
        'dirty': '#f39c12',       # Orange - dirty/mutable data  
        'text': '#ffffff',        # White text
        'bg': '#1a1a1a',         # Dark background
        'accent': '#00d4aa'       # Green accent
    }
    
    fig.patch.set_facecolor(colors['bg'])
    ax.set_facecolor(colors['bg'])
    
    # Column headers
    ax.text(3, 5.5, 'Base Map\n(Immutable)', ha='center', va='center', 
            fontsize=14, weight='bold', color=colors['base'])
    ax.text(9, 5.5, 'Dirty Entries\n(Pending Changes)', ha='center', va='center', 
            fontsize=14, weight='bold', color=colors['dirty'])
    
    # Base map entries (left column)
    base_entries = [
        ("key1: value1", 4.5),
        ("key2: value2", 3.8),
        ("key3: value3", 3.1),
        ("key4: value4", 2.4),
    ]
    
    for entry, y in base_entries:
        rect = FancyBboxPatch((1.5, y-0.3), 3, 0.6,
                              boxstyle="round,pad=0.1",
                              facecolor=colors['base'],
                              edgecolor='white',
                              linewidth=1.5)
        ax.add_patch(rect)
        ax.text(3, y, entry, ha='center', va='center', fontsize=14, 
                family='monospace', weight='bold', color='white')
    
    # Empty dirty entries column (right column)
    empty_box = FancyBboxPatch((7.5, 2.7), 3, 2,
                               boxstyle="round,pad=0.1",
                               facecolor=colors['bg'],
                               edgecolor=colors['dirty'],
                               linewidth=2,
                               linestyle='--')
    ax.add_patch(empty_box)
    ax.text(9, 3.7, 'Empty\n(No pending changes)', ha='center', va='center', 
            fontsize=14, style='italic', color=colors['text'], alpha=0.7)
    
    # Add explanatory text
    ax.text(6, 1.2, 'Clean state: All data comes from the immutable base map\nNo changes are pending, so the dirty entries are empty',
            ha='center', va='center', fontsize=12, style='italic', color=colors['text'], alpha=0.8)
    
    # Add arrows showing data flow
    ax.annotate('Read operations access base map directly', 
                xy=(3, 3.5), xytext=(1, 1.8),
                arrowprops=dict(arrowstyle='->', lw=2, color=colors['accent']),
                fontsize=12, color=colors['accent'], weight='bold')
    
    ax.set_xlim(0, 12)
    ax.set_ylim(1, 6)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('lsp-presentation/dirty-map-clean.png', dpi=300, bbox_inches='tight',
                facecolor=colors['bg'], edgecolor='none')
    plt.close()

def create_dirty_map_with_changes():
    """Create a diagram showing dirty.Map with pending changes"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    
    # Color scheme matching other diagrams
    colors = {
        'base': '#9b59b6',        # Purple - base/immutable data
        'dirty': '#f39c12',       # Orange - dirty/mutable data  
        'text': '#ffffff',        # White text
        'bg': '#1a1a1a',         # Dark background
        'accent': '#00d4aa',      # Green accent
        'modified': '#e74c3c'     # Red for modifications
    }
    
    fig.patch.set_facecolor(colors['bg'])
    ax.set_facecolor(colors['bg'])
    
    # Column headers
    ax.text(3, 5.5, 'Base Map\n(Immutable)', ha='center', va='center', 
            fontsize=14, weight='bold', color=colors['base'])
    ax.text(9, 5.5, 'Dirty Entries\n(Pending Changes)', ha='center', va='center', 
            fontsize=14, weight='bold', color=colors['dirty'])
    
    # Base map entries (left column)
    base_entries = [
        ("key1: value1", 4.5, False),  # Not modified
        ("key2: value2", 3.8, True),   # This one is modified
        ("key3: value3", 3.1, False),  # Not modified
        ("key4: value4", 2.4, False),  # Not modified
    ]
    
    for entry, y, is_modified in base_entries:
        if is_modified:
            # Dimmed style for entries that have been overridden
            rect = FancyBboxPatch((1.5, y-0.3), 3, 0.6,
                                  boxstyle="round,pad=0.1",
                                  facecolor=colors['base'],
                                  edgecolor='white',
                                  linewidth=1.5,
                                  alpha=0.4)
            ax.add_patch(rect)
            ax.text(3, y, entry, ha='center', va='center', fontsize=14, 
                    family='monospace', color='white', alpha=0.5, style='italic')
        else:
            # Normal style for unmodified entries
            rect = FancyBboxPatch((1.5, y-0.3), 3, 0.6,
                                  boxstyle="round,pad=0.1",
                                  facecolor=colors['base'],
                                  edgecolor='white',
                                  linewidth=1.5)
            ax.add_patch(rect)
            ax.text(3, y, entry, ha='center', va='center', fontsize=14, 
                    family='monospace', weight='bold', color='white')
    
    # Dirty entries (right column)
    dirty_rect = FancyBboxPatch((7.5, 3.5), 3, 0.6,
                                boxstyle="round,pad=0.1",
                                facecolor=colors['dirty'],
                                edgecolor='white',
                                linewidth=1.5)
    ax.add_patch(dirty_rect)
    ax.text(9, 3.8, 'key2: new_value', ha='center', va='center', fontsize=14, 
            family='monospace', weight='bold', color='white')
    
    # Add "CLONE" indicator
    ax.text(9, 3.4, '(cloned & modified)', ha='center', va='center', fontsize=10, 
            style='italic', color=colors['text'], alpha=0.7)
    
    # Arrow showing the clone relationship
    ax.annotate('', xy=(7.5, 3.8), xytext=(4.5, 3.8),
               arrowprops=dict(arrowstyle='->', lw=3, color=colors['modified']))
    ax.text(6, 4.1, 'clone & modify', ha='center', va='center', fontsize=12, 
            weight='bold', color=colors['modified'])
    
    # Add explanatory text
    ax.text(6, 1.2, 'When a change is made, the entry is cloned to the dirty map\nReads for that key now come from the dirty entry instead',
            ha='center', va='center', fontsize=12, style='italic', color=colors['text'], alpha=0.8)
    
    # Add read flow arrows
    # Arrow for unmodified entries (read from base)
    ax.annotate('Unmodified entries\nread from base', 
                xy=(2, 2.7), xytext=(0.5, 1.8),
                arrowprops=dict(arrowstyle='->', lw=2, color=colors['accent']),
                fontsize=10, color=colors['accent'], weight='bold', ha='center')
    
    # Arrow for modified entries (read from dirty)
    ax.annotate('Modified entry\nreads from dirty', 
                xy=(9.5, 3.8), xytext=(11, 2.5),
                arrowprops=dict(arrowstyle='->', lw=2, color=colors['dirty']),
                fontsize=10, color=colors['dirty'], weight='bold', ha='center')
    
    ax.set_xlim(0, 12)
    ax.set_ylim(1, 6)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('lsp-presentation/dirty-map-changes.png', dpi=300, bbox_inches='tight',
                facecolor=colors['bg'], edgecolor='none')
    plt.close()

def create_dirty_map_finalization():
    """Create a diagram showing dirty.Map finalization process"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 9))
    
    # Color scheme matching other diagrams
    colors = {
        'base': '#9b59b6',        # Purple - base/immutable data
        'dirty': '#f39c12',       # Orange - dirty/mutable data  
        'text': '#ffffff',        # White text
        'bg': '#1a1a1a',         # Dark background
        'accent': '#00d4aa',      # Green accent
        'output': '#27ae60'       # Darker green for final result
    }
    
    fig.patch.set_facecolor(colors['bg'])
    ax.set_facecolor(colors['bg'])
    
    # Base map (top left) - much larger boxes
    ax.text(2.5, 7.5, 'Base Map', ha='center', va='center', 
            fontsize=16, weight='bold', color=colors['base'])
    base_before = [
        ("key1: value1", 6.8),
        ("key2: value2", 6.2),
        ("key3: value3", 5.6),
    ]
    for entry, y in base_before:
        rect = FancyBboxPatch((0.5, y-0.25), 4, 0.5,
                              boxstyle="round,pad=0.1",
                              facecolor=colors['base'],
                              edgecolor='white',
                              linewidth=2)
        ax.add_patch(rect)
        ax.text(2.5, y, entry, ha='center', va='center', fontsize=13, 
                family='monospace', color='white', weight='bold')
    
    # Dirty entries (top right) - much larger
    ax.text(7.5, 7.5, 'Dirty Entries', ha='center', va='center', 
            fontsize=16, weight='bold', color=colors['dirty'])
    dirty_rect = FancyBboxPatch((5.5, 6.0), 4, 0.5,
                                boxstyle="round,pad=0.1",
                                facecolor=colors['dirty'],
                                edgecolor='white',
                                linewidth=2)
    ax.add_patch(dirty_rect)
    ax.text(7.5, 6.25, 'key2: new_value', ha='center', va='center', fontsize=13, 
            family='monospace', color='white', weight='bold')
    
    # Finalization arrow - larger and more prominent
    ax.annotate('', xy=(5, 3.8), xytext=(5, 4.8),
               arrowprops=dict(arrowstyle='->', lw=6, color=colors['accent']))
    ax.text(6.5, 4.3, 'FINALIZE', ha='center', va='center', fontsize=16, 
            weight='bold', color=colors['accent'])
    
    # New immutable map (bottom center) - much larger boxes
    ax.text(5, 3.2, 'New Immutable Map', ha='center', va='center', 
            fontsize=16, weight='bold', color=colors['output'])
    
    new_map_entries = [
        ("key1: value1", 2.5, False),      # Unchanged
        ("key2: new_value", 1.9, True),    # Changed
        ("key3: value3", 1.3, False),      # Unchanged
    ]
    
    for entry, y, was_changed in new_map_entries:
        if was_changed:
            # Use dirty/orange color for changed entries to match dirty color
            rect = FancyBboxPatch((3, y-0.25), 4, 0.5,
                                  boxstyle="round,pad=0.1",
                                  facecolor=colors['dirty'],
                                  edgecolor='white',
                                  linewidth=2)
            ax.add_patch(rect)
            ax.text(5, y, entry, ha='center', va='center', fontsize=13, 
                    family='monospace', weight='bold', color='white')
        else:
            # Normal style for unchanged entries
            rect = FancyBboxPatch((3, y-0.25), 4, 0.5,
                                  boxstyle="round,pad=0.1",
                                  facecolor=colors['base'],
                                  edgecolor='white',
                                  linewidth=2)
            ax.add_patch(rect)
            ax.text(5, y, entry, ha='center', va='center', fontsize=13, 
                    family='monospace', color='white', weight='bold')
    
    # Add explanatory notes - larger and better positioned
    ax.text(10.5, 6.5, 'Dirty entries\noverride base\nentries', 
            ha='center', va='center', fontsize=13, style='italic', color=colors['text'], alpha=0.8)
    
    ax.text(10.5, 1.9, 'Result is a new\nimmutable map\nwith all changes\napplied', 
            ha='center', va='center', fontsize=13, style='italic', color=colors['text'], alpha=0.8)
    
    # Add process flow arrows - more prominent
    ax.annotate('', xy=(4, 1.9), xytext=(6.5, 6.25),
               arrowprops=dict(arrowstyle='->', lw=3, color=colors['dirty'], linestyle='--'))
    
    ax.annotate('', xy=(4, 1.3), xytext=(2.5, 5.6),
               arrowprops=dict(arrowstyle='->', lw=3, color=colors['base'], linestyle='--'))
    
    ax.set_xlim(0, 12)
    ax.set_ylim(0.8, 8)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('lsp-presentation/dirty-map-finalization.png', dpi=300, bbox_inches='tight',
                facecolor=colors['bg'], edgecolor='none')
    plt.close()

def main():
    """Generate dirty.Map visualization diagrams"""
    print("Generating dirty.Map visualization diagrams...")
    
    diagrams = [
        ("Clean State", create_dirty_map_clean_state),
        ("With Changes", create_dirty_map_with_changes),
        ("Finalization Process", create_dirty_map_finalization),
    ]
    
    for name, func in diagrams:
        print(f"  Creating {name}...")
        func()
        print(f"  ✓ {name} saved")
    
    print("\ndirty.Map diagrams generated successfully!")
    print("\nGenerated files:")
    print("  - lsp-presentation/dirty-map-clean.png")
    print("  - lsp-presentation/dirty-map-changes.png")
    print("  - lsp-presentation/dirty-map-finalization.png")

if __name__ == "__main__":
    main()
