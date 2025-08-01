#!/usr/bin/env python3
"""
LSP request flow visualization for typescript-go presentation
Shows the complete flow from LSP request to language service response
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch
import matplotlib.patheffects as path_effects

# Set up the matplotlib style
plt.style.use('default')
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'sans-serif'

def create_lsp_request_flow():
    """Create a diagram showing the complete LSP request flow"""
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    
    # Color scheme matching other diagrams
    colors = {
        'request': '#3498db',       # Blue - incoming request
        'condition': '#f39c12',     # Orange - decision points
        'snapshot': '#9b59b6',      # Purple - snapshot operations
        'mutex': '#e74c3c',         # Red - mutex/locking
        'background': '#27ae60',    # Green - background operations
        'text': '#ffffff',          # White text
        'bg': '#1a1a1a',           # Dark background
        'accent': '#00d4aa'         # Teal accent
    }
    
    fig.patch.set_facecolor(colors['bg'])
    ax.set_facecolor(colors['bg'])
    
    # Starting point
    start_box = FancyBboxPatch((1, 8.5), 4, 0.8,
                               boxstyle="round,pad=0.05",
                               facecolor=colors['request'],
                               edgecolor='white',
                               linewidth=2)
    ax.add_patch(start_box)
    ax.text(3, 8.9, 'LSP Request (GetLanguageService)\nflushChanges() 🔒', ha='center', va='center', 
            fontsize=13, weight='bold', color='white')
    
    # Decision diamond - has changes?
    diamond_points = [(3, 7.6), (4.5, 6.8), (3, 6.0), (1.5, 6.8)]
    diamond = patches.Polygon(diamond_points, closed=True, 
                             facecolor=colors['condition'], 
                             edgecolor='white', linewidth=2)
    ax.add_patch(diamond)
    ax.text(3, 6.8, 'Has file changes\nor ATA changes?', ha='center', va='center', 
            fontsize=12, weight='bold', color='white')
    
    # Combined UpdateSnapshot box - used by both paths
    update_box = FancyBboxPatch((6, 5.5), 4.5, 2,
                               boxstyle="round,pad=0.05",
                               facecolor=colors['snapshot'],
                               edgecolor='white',
                               linewidth=2)
    ax.add_patch(update_box)
    ax.text(8.25, 6.5, 'UpdateSnapshot()\n🔒 snapshotMu.Lock()\n\n• Clone snapshot • Apply changes\n• Include requestedURIs\n• Guarantees project loaded', 
            ha='center', va='center', fontsize=12, weight='bold', color='white')
    
    # NO path - Use current snapshot
    no_box = FancyBboxPatch((0.5, 4.5), 3, 0.8,
                            boxstyle="round,pad=0.05",
                            facecolor=colors['snapshot'],
                            edgecolor='white',
                            linewidth=2)
    ax.add_patch(no_box)
    ax.text(2, 4.9, 'Use current snapshot\n🔒 snapshotMu.RLock()', ha='center', va='center', 
            fontsize=12, weight='bold', color='white')
    
    # Project check diamond - only for NO path
    project_diamond_points = [(2, 3.6), (3.2, 3.0), (2, 2.4), (0.8, 3.0)]
    project_diamond = patches.Polygon(project_diamond_points, closed=True, 
                                     facecolor=colors['condition'], 
                                     edgecolor='white', linewidth=2)
    ax.add_patch(project_diamond)
    ax.text(2, 3.0, 'Project loaded\n& up-to-date?', ha='center', va='center', 
            fontsize=12, weight='bold', color='white')
    
    # Final result
    result_box = FancyBboxPatch((6, 1.5), 4.5, 0.8,
                                boxstyle="round,pad=0.05",
                                facecolor=colors['request'],
                                edgecolor='white',
                                linewidth=2)
    ax.add_patch(result_box)
    ax.text(8.25, 1.9, 'Return project.LanguageService', ha='center', va='center', 
            fontsize=14, weight='bold', color='white')
    
    # Side effect boxes - connected with dotted lines
    # Ref counting details
    ref_box = FancyBboxPatch((12, 7), 3.5, 1.8,
                             boxstyle="round,pad=0.05",
                             facecolor=colors['mutex'],
                             edgecolor='white',
                             linewidth=2)
    ax.add_patch(ref_box)
    ax.text(13.75, 7.9, 'Ref Counting:\n• programCounter.Ref()\n• extendedConfigCache.Ref()\n• oldSnapshot.Deref()\n• dispose if refCount = 0', 
            ha='center', va='center', fontsize=11, weight='bold', color='white')
    
    # Background tasks
    bg_box = FancyBboxPatch((12, 4.5), 3.5, 2.2,
                            boxstyle="round,pad=0.05",
                            facecolor=colors['background'],
                            edgecolor='white',
                            linewidth=2)
    ax.add_patch(bg_box)
    ax.text(13.75, 5.6, 'Background Tasks:\n• Logging: builder logs,\n  project changes\n• File Watching: update watchers\n• ATA: trigger\n• Diagnostics: refresh', 
            ha='center', va='center', fontsize=11, weight='bold', color='white')
    
    # Main flow arrows
    ax.annotate('', xy=(3, 7.6), xytext=(3, 8.3),
               arrowprops=dict(arrowstyle='->', lw=3, color=colors['accent']))
    
    # YES arrow - directly to UpdateSnapshot
    ax.annotate('YES', xy=(6.5, 6.5), xytext=(4.5, 6.8),
               arrowprops=dict(arrowstyle='->', lw=3, color=colors['accent']),
               fontsize=13, weight='bold', color=colors['accent'])
    
    # NO arrow
    ax.annotate('NO', xy=(2, 5.3), xytext=(1.5, 6.8),
               arrowprops=dict(arrowstyle='->', lw=3, color=colors['accent']),
               fontsize=13, weight='bold', color=colors['accent'])
    
    # NO path to project check
    ax.annotate('', xy=(2, 3.6), xytext=(2, 4.3),
               arrowprops=dict(arrowstyle='->', lw=3, color=colors['accent']))
    
    # Project NOT ready - goes to UpdateSnapshot
    ax.annotate('NO', xy=(6, 5.8), xytext=(3.2, 3.0),
               arrowprops=dict(arrowstyle='->', lw=3, color=colors['accent'], connectionstyle="arc3,rad=0.2"),
               fontsize=13, weight='bold', color=colors['accent'])
    
    # Project IS ready - bypasses UpdateSnapshot, goes directly to result
    ax.annotate('YES', xy=(6.5, 1.9), xytext=(2.8, 2.6),
               arrowprops=dict(arrowstyle='->', lw=3, color=colors['accent'], connectionstyle="arc3,rad=0.4"),
               fontsize=13, weight='bold', color=colors['accent'])
    
    # UpdateSnapshot to result
    ax.annotate('', xy=(8.25, 2.3), xytext=(8.25, 5.5),
               arrowprops=dict(arrowstyle='->', lw=4, color=colors['accent']))
    
    # Dotted arrows for side effects from UpdateSnapshot
    ax.annotate('', xy=(12, 7.9), xytext=(10.5, 6.8),
               arrowprops=dict(arrowstyle='->', lw=2, color=colors['mutex'], linestyle='--'))
    
    ax.annotate('', xy=(12, 5.6), xytext=(10.5, 6.2),
               arrowprops=dict(arrowstyle='->', lw=2, color=colors['background'], linestyle='--'))
    
    # Add side notes
    ax.text(0.5, 7.5, '🔒 Mutexes ensure\nthread safety', ha='left', va='center', 
            fontsize=11, style='italic', color=colors['text'], alpha=0.8)
    
    ax.text(0.5, 0.8, '⚠️ Key insight: At most ONE snapshot update per request!\nIf update happened but project still not ready → PANIC', 
            ha='left', va='center', fontsize=11, style='italic', color='#ffeb3b', alpha=0.9, weight='bold')
    
    ax.set_xlim(0, 16)
    ax.set_ylim(0.5, 9.5)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('lsp-presentation/lsp-request-flow.png', dpi=300, bbox_inches='tight',
                facecolor=colors['bg'], edgecolor='none')
    plt.close()

def create_snapshot_lifecycle():
    """Create a diagram showing snapshot lifecycle and ref counting"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    
    # Color scheme
    colors = {
        'snapshot': '#9b59b6',      # Purple - snapshots
        'ref': '#27ae60',           # Green - ref counting
        'dispose': '#e74c3c',       # Red - disposal
        'text': '#ffffff',          # White text
        'bg': '#1a1a1a',           # Dark background
        'accent': '#00d4aa'         # Teal accent
    }
    
    fig.patch.set_facecolor(colors['bg'])
    ax.set_facecolor(colors['bg'])
    
    # Old snapshot
    old_snap = FancyBboxPatch((1, 6), 3, 1.5,
                              boxstyle="round,pad=0.1",
                              facecolor=colors['snapshot'],
                              edgecolor='white',
                              linewidth=2)
    ax.add_patch(old_snap)
    ax.text(2.5, 6.75, 'Old Snapshot\nrefCount: 1', ha='center', va='center', 
            fontsize=12, weight='bold', color='white')
    
    # Clone operation
    clone_box = FancyBboxPatch((6, 6.5), 3, 2,
                               boxstyle="round,pad=0.1",
                               facecolor=colors['ref'],
                               edgecolor='white',
                               linewidth=2)
    ax.add_patch(clone_box)
    ax.text(7.5, 7.5, 'snapshot.Clone()\n• Create new snapshot\n• Ref new programs\n• Ref extended configs', 
            ha='center', va='center', fontsize=10, weight='bold', color='white')
    
    # New snapshot
    new_snap = FancyBboxPatch((10, 6), 3, 1.5,
                              boxstyle="round,pad=0.1",
                              facecolor=colors['snapshot'],
                              edgecolor='white',
                              linewidth=2)
    ax.add_patch(new_snap)
    ax.text(11.5, 6.75, 'New Snapshot\nrefCount: 1', ha='center', va='center', 
            fontsize=12, weight='bold', color='white')
    
    # Deref operation
    deref_box = FancyBboxPatch((3, 3.5), 4, 1.5,
                               boxstyle="round,pad=0.1",
                               facecolor=colors['dispose'],
                               edgecolor='white',
                               linewidth=2)
    ax.add_patch(deref_box)
    ax.text(5, 4.25, 'oldSnapshot.Deref()\nreturns true if refCount == 0\n(ready for disposal)', 
            ha='center', va='center', fontsize=10, weight='bold', color='white')
    
    # Disposal
    dispose_box = FancyBboxPatch((8, 2), 5, 1.5,
                                 boxstyle="round,pad=0.1",
                                 facecolor=colors['dispose'],
                                 edgecolor='white',
                                 linewidth=2)
    ax.add_patch(dispose_box)
    ax.text(10.5, 2.75, 'oldSnapshot.dispose()\n• Deref programs in program counter\n• Deref extended config cache entries\n• Free memory', 
            ha='center', va='center', fontsize=10, weight='bold', color='white')
    
    # Arrows
    ax.annotate('', xy=(6, 7.5), xytext=(4, 6.75),
               arrowprops=dict(arrowstyle='->', lw=3, color=colors['accent']))
    
    ax.annotate('', xy=(10, 6.75), xytext=(9, 7.5),
               arrowprops=dict(arrowstyle='->', lw=3, color=colors['accent']))
    
    ax.annotate('', xy=(5, 5), xytext=(2.5, 6),
               arrowprops=dict(arrowstyle='->', lw=2, color=colors['dispose']))
    
    ax.annotate('if refCount == 0', xy=(8, 3), xytext=(6.5, 4),
               arrowprops=dict(arrowstyle='->', lw=2, color=colors['dispose']),
               fontsize=10, weight='bold', color=colors['dispose'])
    
    # Labels
    ax.text(7, 1, '💡 Ref counting prevents memory leaks by ensuring snapshots\nare only disposed when no longer referenced', 
            ha='center', va='center', fontsize=11, style='italic', color=colors['text'], alpha=0.8)
    
    ax.set_xlim(0, 14)
    ax.set_ylim(0.5, 8.5)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('lsp-presentation/snapshot-lifecycle.png', dpi=300, bbox_inches='tight',
                facecolor=colors['bg'], edgecolor='none')
    plt.close()

def main():
    """Generate LSP request flow diagrams"""
    print("Generating LSP request flow diagrams...")
    
    diagrams = [
        ("LSP Request Flow", create_lsp_request_flow),
        ("Snapshot Lifecycle", create_snapshot_lifecycle),
    ]
    
    for name, func in diagrams:
        print(f"  Creating {name}...")
        func()
        print(f"  ✓ {name} saved")
    
    print("\nLSP request flow diagrams generated successfully!")
    print("\nGenerated files:")
    print("  - lsp-presentation/lsp-request-flow.png")
    print("  - lsp-presentation/snapshot-lifecycle.png")

if __name__ == "__main__":
    main()
