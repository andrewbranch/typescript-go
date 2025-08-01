#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

def create_builder_hierarchy():
    """Create a diagram showing the hierarchy of builder objects and their dirty maps"""
    fig, ax = plt.subplots(1, 1, figsize=(18, 12))
    
    # Color scheme matching other diagrams
    colors = {
        'snapshot': '#9b59b6',      # Purple - snapshot
        'builder': '#3498db',       # Blue - builders
        'dirty_map': '#e74c3c',     # Red - dirty maps
        'finalized': '#27ae60',     # Green - finalized objects
        'text': '#ffffff',          # White text
        'bg': '#1a1a1a',           # Dark background
        'accent': '#00d4aa',        # Teal accent
        'arrow': '#f39c12'          # Orange arrows
    }
    
    fig.patch.set_facecolor(colors['bg'])
    ax.set_facecolor(colors['bg'])
    
    # Title
    ax.text(9, 11, 'Snapshot Cloning: Builder Hierarchy & Dirty Maps', 
            ha='center', va='center', fontsize=18, weight='bold', color=colors['text'])
    
    # Original Snapshot
    snapshot_box = FancyBboxPatch((1, 9.5), 4, 1,
                                  boxstyle="round,pad=0.05",
                                  facecolor=colors['snapshot'],
                                  edgecolor='white',
                                  linewidth=2)
    ax.add_patch(snapshot_box)
    ax.text(3, 10, 'Original Snapshot\n(Immutable)', ha='center', va='center', 
            fontsize=14, weight='bold', color='white')
    
    # Arrow to clone operation
    ax.annotate('Clone Operation', xy=(7, 10), xytext=(5.5, 10),
               arrowprops=dict(arrowstyle='->', lw=3, color=colors['arrow']),
               fontsize=12, weight='bold', color=colors['arrow'])
    
    # New Snapshot (being built)
    new_snapshot_box = FancyBboxPatch((13, 9.5), 4, 1,
                                      boxstyle="round,pad=0.05",
                                      facecolor=colors['snapshot'],
                                      edgecolor='white',
                                      linewidth=2)
    ax.add_patch(new_snapshot_box)
    ax.text(15, 10, 'New Snapshot\n(Under Construction)', ha='center', va='center', 
            fontsize=14, weight='bold', color='white')
    
    # Builder 1: snapshotFSBuilder
    fs_builder_box = FancyBboxPatch((1, 7.5), 5, 1.2,
                                    boxstyle="round,pad=0.05",
                                    facecolor=colors['builder'],
                                    edgecolor='white',
                                    linewidth=2)
    ax.add_patch(fs_builder_box)
    ax.text(3.5, 8.1, 'snapshotFSBuilder\nManages filesystem state', ha='center', va='center', 
            fontsize=16, weight='bold', color='white')
    
    # Dirty map for FS
    fs_dirty_box = FancyBboxPatch((7.5, 7.5), 4, 1.2,
                                  boxstyle="round,pad=0.05",
                                  facecolor=colors['dirty_map'],
                                  edgecolor='white',
                                  linewidth=2)
    ax.add_patch(fs_dirty_box)
    ax.text(9.5, 8.1, 'dirty.Map[string, File]\nDisk file changes', ha='center', va='center', 
            fontsize=14, weight='bold', color='white')
    
    # Finalized FS
    fs_final_box = FancyBboxPatch((13, 7.5), 4, 1.2,
                                  boxstyle="round,pad=0.05",
                                  facecolor=colors['finalized'],
                                  edgecolor='white',
                                  linewidth=2)
    ax.add_patch(fs_final_box)
    ax.text(15, 8.1, 'Finalized FS\nImmutable file system', ha='center', va='center', 
            fontsize=14, weight='bold', color='white')
    
    # Builder 2: projectCollectionBuilder
    proj_builder_box = FancyBboxPatch((1, 5.5), 5, 1.2,
                                      boxstyle="round,pad=0.05",
                                      facecolor=colors['builder'],
                                      edgecolor='white',
                                      linewidth=2)
    ax.add_patch(proj_builder_box)
    ax.text(3.5, 6.1, 'projectCollectionBuilder\nManages project collection', ha='center', va='center', 
            fontsize=16, weight='bold', color='white')
    
    # Dirty map for projects
    proj_dirty_box = FancyBboxPatch((7.5, 5.5), 4, 1.2,
                                    boxstyle="round,pad=0.05",
                                    facecolor=colors['dirty_map'],
                                    edgecolor='white',
                                    linewidth=2)
    ax.add_patch(proj_dirty_box)
    ax.text(9.5, 6.1, 'dirty.Map[string, Project]\nProject changes', ha='center', va='center', 
            fontsize=14, weight='bold', color='white')
    
    # Finalized projects
    proj_final_box = FancyBboxPatch((13, 5.5), 4, 1.2,
                                    boxstyle="round,pad=0.05",
                                    facecolor=colors['finalized'],
                                    edgecolor='white',
                                    linewidth=2)
    ax.add_patch(proj_final_box)
    ax.text(15, 6.1, 'Finalized Projects\nImmutable project map', ha='center', va='center', 
            fontsize=14, weight='bold', color='white')
    
    # Builder 3: configFileRegistryBuilder
    config_builder_box = FancyBboxPatch((1, 3.5), 5, 1.2,
                                        boxstyle="round,pad=0.05",
                                        facecolor=colors['builder'],
                                        edgecolor='white',
                                        linewidth=2)
    ax.add_patch(config_builder_box)
    ax.text(3.5, 4.1, 'configFileRegistryBuilder\nManages config file registry', ha='center', va='center', 
            fontsize=16, weight='bold', color='white')
    
    # Dirty maps for config (two maps!)
    config_entries_box = FancyBboxPatch((7, 4), 3, 0.8,
                                        boxstyle="round,pad=0.05",
                                        facecolor=colors['dirty_map'],
                                        edgecolor='white',
                                        linewidth=2)
    ax.add_patch(config_entries_box)
    ax.text(8.5, 4.4, 'dirty.Map[string,\nConfigFileEntry]', ha='center', va='center', 
            fontsize=13, weight='bold', color='white')
    
    config_names_box = FancyBboxPatch((7, 2.8), 3, 0.8,
                                      boxstyle="round,pad=0.05",
                                      facecolor=colors['dirty_map'],
                                      edgecolor='white',
                                      linewidth=2)
    ax.add_patch(config_names_box)
    ax.text(8.5, 3.2, 'dirty.Map[string,\nConfigFileName]', ha='center', va='center', 
            fontsize=13, weight='bold', color='white')
    
    # Finalized config
    config_final_box = FancyBboxPatch((13, 3.5), 4, 1.2,
                                      boxstyle="round,pad=0.05",
                                      facecolor=colors['finalized'],
                                      edgecolor='white',
                                      linewidth=2)
    ax.add_patch(config_final_box)
    ax.text(15, 4.1, 'Finalized Config Registry\nImmutable config maps', ha='center', va='center', 
            fontsize=14, weight='bold', color='white')
    
    # Arrows showing the flow
    # Builder to dirty map arrows
    ax.annotate('', xy=(7.5, 8.1), xytext=(6, 8.1),
               arrowprops=dict(arrowstyle='->', lw=2, color=colors['accent']))
    ax.annotate('', xy=(7.5, 6.1), xytext=(6, 6.1),
               arrowprops=dict(arrowstyle='->', lw=2, color=colors['accent']))
    ax.annotate('', xy=(7, 4.1), xytext=(6, 4.1),
               arrowprops=dict(arrowstyle='->', lw=2, color=colors['accent']))
    
    # Dirty map to finalized arrows
    ax.annotate('', xy=(13, 8.1), xytext=(11.5, 8.1),
               arrowprops=dict(arrowstyle='->', lw=2, color=colors['accent']))
    ax.annotate('', xy=(13, 6.1), xytext=(11.5, 6.1),
               arrowprops=dict(arrowstyle='->', lw=2, color=colors['accent']))
    ax.annotate('', xy=(13, 4.1), xytext=(10, 3.6),
               arrowprops=dict(arrowstyle='->', lw=2, color=colors['accent'], connectionstyle="arc3,rad=0.1"))
    
    # Finalized to new snapshot arrows
    ax.annotate('', xy=(15, 9.5), xytext=(15, 8.7),
               arrowprops=dict(arrowstyle='->', lw=2, color=colors['accent']))
    ax.annotate('', xy=(15, 9.5), xytext=(15, 7.3),
               arrowprops=dict(arrowstyle='->', lw=2, color=colors['accent']))
    ax.annotate('', xy=(15, 9.5), xytext=(15, 5.3),
               arrowprops=dict(arrowstyle='->', lw=2, color=colors['accent']))
    
    # Labels for the flow
    ax.text(6.75, 8.5, 'uses', ha='center', va='center', fontsize=11, 
            style='italic', color=colors['text'], alpha=0.8)
    ax.text(6.75, 6.5, 'uses', ha='center', va='center', fontsize=11, 
            style='italic', color=colors['text'], alpha=0.8)
    ax.text(6.75, 4.5, 'uses', ha='center', va='center', fontsize=11, 
            style='italic', color=colors['text'], alpha=0.8)
    
    ax.text(12.25, 8.5, 'produces', ha='center', va='center', fontsize=11, 
            style='italic', color=colors['text'], alpha=0.8)
    ax.text(12.25, 6.5, 'produces', ha='center', va='center', fontsize=11, 
            style='italic', color=colors['text'], alpha=0.8)
    ax.text(12.25, 4.5, 'produces', ha='center', va='center', fontsize=11, 
            style='italic', color=colors['text'], alpha=0.8)
    
    ax.text(15.5, 9, 'combine', ha='center', va='center', fontsize=11, 
            style='italic', color=colors['text'], alpha=0.8, rotation=90)
    
    # Key insights
    insights_box = FancyBboxPatch((1, 1), 16, 1.5,
                                  boxstyle="round,pad=0.05",
                                  facecolor=colors['bg'],
                                  edgecolor=colors['accent'],
                                  linewidth=2)
    ax.add_patch(insights_box)
    ax.text(9, 1.75, '🔑 Key Insights:', ha='center', va='center', 
            fontsize=14, weight='bold', color=colors['accent'])
    ax.text(9, 1.25, '• Each builder manages one aspect of the snapshot (filesystem, projects, configs)\n• Dirty maps track only what changed since the original snapshot\n• Finalized objects are immutable and become part of the new snapshot\n• Pattern enables efficient copy-on-write semantics', 
            ha='center', va='center', fontsize=12, color=colors['text'])
    
    ax.set_xlim(0, 18)
    ax.set_ylim(0.5, 11.5)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('lsp-presentation/builder-hierarchy.png', dpi=300, bbox_inches='tight',
                facecolor=colors['bg'], edgecolor='none')
    plt.close()

def create_builder_lifecycle():
    """Create a complementary diagram showing the lifecycle of the building process"""
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    
    # Color scheme matching other diagrams
    colors = {
        'phase': '#3498db',         # Blue - phases
        'operation': '#f39c12',     # Orange - operations
        'state': '#9b59b6',         # Purple - states
        'text': '#ffffff',          # White text
        'bg': '#1a1a1a',           # Dark background
        'accent': '#00d4aa'         # Teal accent
    }
    
    fig.patch.set_facecolor(colors['bg'])
    ax.set_facecolor(colors['bg'])
    
    # Title
    ax.text(8, 9.5, 'Builder Lifecycle: From Clone to Finalize', 
            ha='center', va='center', fontsize=18, weight='bold', color=colors['text'])
    
    # Phase 1: Initialization
    phase1_box = FancyBboxPatch((1, 7.5), 4.5, 1.5,
                                boxstyle="round,pad=0.05",
                                facecolor=colors['phase'],
                                edgecolor='white',
                                linewidth=2)
    ax.add_patch(phase1_box)
    ax.text(3.25, 8.25, '1. Initialize Builders\n• snapshotFSBuilder\n• projectCollectionBuilder\n• configFileRegistryBuilder', 
            ha='center', va='center', fontsize=15, weight='bold', color='white')
    
    # Phase 2: Apply Changes
    phase2_box = FancyBboxPatch((6.5, 7.5), 4.5, 1.5,
                                boxstyle="round,pad=0.05",
                                facecolor=colors['operation'],
                                edgecolor='white',
                                linewidth=2)
    ax.add_patch(phase2_box)
    ax.text(8.75, 8.25, '2. Apply Changes\n• File modifications\n• Project updates\n• Config changes', 
            ha='center', va='center', fontsize=15, weight='bold', color='white')
    
    # Phase 3: Finalize
    phase3_box = FancyBboxPatch((12, 7.5), 4.5, 1.5,
                                boxstyle="round,pad=0.05",
                                facecolor=colors['state'],
                                edgecolor='white',
                                linewidth=2)
    ax.add_patch(phase3_box)
    ax.text(14.25, 8.25, '3. Finalize All\n• Build immutable maps\n• Create new snapshot\n• Return result', 
            ha='center', va='center', fontsize=15, weight='bold', color='white')
    
    # Arrows between phases
    ax.annotate('', xy=(6.5, 8.25), xytext=(5.5, 8.25),
               arrowprops=dict(arrowstyle='->', lw=3, color=colors['accent']))
    ax.annotate('', xy=(12, 8.25), xytext=(11, 8.25),
               arrowprops=dict(arrowstyle='->', lw=3, color=colors['accent']))
    
    # Detailed breakdown for each builder type
    y_positions = [5.5, 4, 2.5]
    builder_names = ['File System Builder', 'Project Collection Builder', 'Config Registry Builder']
    builder_details = [
        '• dirty.Map[string, File]\n• Track file additions/deletions/modifications\n• Merge with original FS on finalize',
        '• dirty.Map[string, Project]\n• Track project state changes\n• Handle project creation/updates',
        '• dirty.Map[string, ConfigFileEntry]\n• dirty.Map[string, ConfigFileName]\n• Dual maps for config management'
    ]
    
    for i, (y, name, details) in enumerate(zip(y_positions, builder_names, builder_details)):
        # Builder name
        name_box = FancyBboxPatch((1, y), 4, 0.8,
                                  boxstyle="round,pad=0.05",
                                  facecolor=colors['phase'],
                                  edgecolor='white',
                                  linewidth=2)
        ax.add_patch(name_box)
        ax.text(3, y + 0.4, name, ha='center', va='center', 
                fontsize=16, weight='bold', color='white')
        
        # Details
        details_box = FancyBboxPatch((5.5, y), 9, 0.8,
                                     boxstyle="round,pad=0.05",
                                     facecolor=colors['bg'],
                                     edgecolor=colors['accent'],
                                     linewidth=1)
        ax.add_patch(details_box)
        ax.text(10, y + 0.4, details, ha='center', va='center', 
                fontsize=13, color=colors['text'])
        
        # Arrow
        ax.annotate('', xy=(5.5, y + 0.4), xytext=(5, y + 0.4),
                   arrowprops=dict(arrowstyle='->', lw=2, color=colors['accent']))
    
    # Bottom note
    ax.text(8, 1, '💡 Efficiency: Only changed data is stored in dirty maps.\nOriginal immutable data is referenced, not copied.', 
            ha='center', va='center', fontsize=12, style='italic', 
            color=colors['accent'], weight='bold')
    
    ax.set_xlim(0, 16)
    ax.set_ylim(0.5, 10)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('lsp-presentation/builder-lifecycle.png', dpi=300, bbox_inches='tight',
                facecolor=colors['bg'], edgecolor='none')
    plt.close()

if __name__ == "__main__":
    print("Generating builder hierarchy diagrams...")
    
    print("  Creating Builder Hierarchy...")
    create_builder_hierarchy()
    print("  ✓ Builder Hierarchy saved")
    
    print("  Creating Builder Lifecycle...")
    create_builder_lifecycle()
    print("  ✓ Builder Lifecycle saved")
    
    print("\nBuilder hierarchy diagrams generated successfully!")
    print("\nGenerated files:")
    print("  - lsp-presentation/builder-hierarchy.png")
    print("  - lsp-presentation/builder-lifecycle.png")
