#!/usr/bin/env python3
"""
Code syntax highlighting generator for typescript-go presentation
Creates nicely formatted code snippets with syntax highlighting
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
from pygments import highlight
from pygments.lexers import GoLexer, TypeScriptLexer, JsonLexer
from pygments.formatters import TerminalFormatter
from pygments.token import Token
import matplotlib.font_manager as fm

# Set up matplotlib for code rendering
plt.rcParams['font.family'] = 'monospace'
plt.rcParams['font.size'] = 10

# Color scheme for syntax highlighting (VS Code Dark+ theme inspired)
COLORS = {
    Token.Keyword: '#569CD6',           # Blue for keywords
    Token.String: '#CE9178',            # Orange for strings
    Token.Comment: '#6A9955',           # Green for comments
    Token.Name.Function: '#DCDCAA',     # Yellow for functions
    Token.Name.Type: '#4EC9B0',         # Teal for types
    Token.Name.Variable: '#9CDCFE',     # Light blue for variables
    Token.Number: '#B5CEA8',            # Light green for numbers
    Token.Operator: '#D4D4D4',          # Light gray for operators
    Token.Punctuation: '#D4D4D4',       # Light gray for punctuation
    Token.Name: '#D4D4D4',              # Default light gray
    Token.Text: '#D4D4D4',              # Default text color
}

def get_token_color(token_type):
    """Get color for a token type, falling back to parent types"""
    for token in COLORS:
        if token_type in token or token in token_type:
            return COLORS[token]
    return COLORS[Token.Text]

def create_code_snippet(code, lexer, title, filename, output_folder="code-examples"):
    """Create a syntax-highlighted code snippet image"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    
    # Set dark background
    fig.patch.set_facecolor('#1E1E1E')
    ax.set_facecolor('#1E1E1E')
    
    # Title
    ax.text(0.5, 0.95, title, transform=ax.transAxes, fontsize=16, 
            weight='bold', color='white', ha='center')
    
    # Filename header (like VS Code tab)
    filename_rect = Rectangle((0.05, 0.88), 0.3, 0.04, 
                             facecolor='#2D2D30', edgecolor='#3E3E42')
    ax.add_patch(filename_rect)
    ax.text(0.06, 0.9, filename, transform=ax.transAxes, fontsize=11,
            color='#CCCCCC', va='center', family='monospace')
    
    # Code area background
    code_rect = Rectangle((0.05, 0.1), 0.9, 0.77, 
                         facecolor='#1E1E1E', edgecolor='#3E3E42', linewidth=1)
    ax.add_patch(code_rect)
    
    # Tokenize the code
    tokens = list(lexer.get_tokens(code))
    
    # Render the code with syntax highlighting
    y_pos = 0.83
    x_pos = 0.07
    line_height = 0.025
    
    current_line = 1
    
    for token_type, text in tokens:
        color = get_token_color(token_type)
        
        # Handle line numbers and newlines
        if '\n' in text:
            lines = text.split('\n')
            for i, line in enumerate(lines):
                if line:  # Don't render empty lines
                    ax.text(x_pos, y_pos, line, transform=ax.transAxes,
                           fontsize=10, color=color, family='monospace', va='top')
                if i < len(lines) - 1:  # Don't move down after the last line
                    y_pos -= line_height
                    current_line += 1
                    x_pos = 0.07
                    # Add line number
                    ax.text(0.055, y_pos + line_height/2, str(current_line), 
                           transform=ax.transAxes, fontsize=9, color='#858585',
                           family='monospace', ha='right', va='center')
        else:
            ax.text(x_pos, y_pos, text, transform=ax.transAxes,
                   fontsize=10, color=color, family='monospace', va='top')
            # Approximate text width for positioning
            x_pos += len(text) * 0.0065
    
    # Add line number for first line
    ax.text(0.055, y_pos + line_height/2, "1", transform=ax.transAxes, 
           fontsize=9, color='#858585', family='monospace', ha='right', va='center')
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig(f'{output_folder}/{filename.replace(".", "_")}.png', 
                dpi=300, bbox_inches='tight', facecolor='#1E1E1E', edgecolor='none')
    plt.close()

def create_dirty_map_go_example():
    """Create an example of dirty.Map usage in Go"""
    code = '''// dirty.Map usage example
type ProjectCollection struct {
    configuredProjects *dirty.Map[tspath.Path, *Project]
    inferredProject    *Project
}

func (pc *ProjectCollection) SetProject(path tspath.Path, project *Project) *ProjectCollection {
    return &ProjectCollection{
        configuredProjects: pc.configuredProjects.Set(path, project),
        inferredProject:    pc.inferredProject,
    }
}

func (pc *ProjectCollection) GetProject(path tspath.Path) *Project {
    if project, exists := pc.configuredProjects.Get(path); exists {
        return project
    }
    return pc.inferredProject
}

func (pc *ProjectCollection) Clone() *ProjectCollection {
    return &ProjectCollection{
        configuredProjects: pc.configuredProjects.Clone(),
        inferredProject:    pc.inferredProject,
    }
}'''
    
    create_code_snippet(code, GoLexer(), 
                       "dirty.Map Usage in ProjectCollection", 
                       "project_collection.go")

def create_snapshot_system_example():
    """Create an example of the snapshot system"""
    code = '''// Snapshot system with reference counting
type Snapshot struct {
    diskFiles           map[tspath.Path]*diskFile
    ProjectCollection   *ProjectCollection
    ConfigFileRegistry  *ConfigFileRegistry
    refCount           atomic.Int32
}

func (s *Snapshot) Ref() {
    s.refCount.Add(1)
}

func (s *Snapshot) Deref() bool {
    return s.refCount.Add(-1) == 0
}

func (s *Snapshot) Clone(ctx context.Context, change SnapshotChange, 
                        session *Session) *Snapshot {
    newSnapshot := &Snapshot{
        diskFiles:          make(map[tspath.Path]*diskFile),
        ProjectCollection:  s.ProjectCollection,
        ConfigFileRegistry: s.ConfigFileRegistry,
    }
    newSnapshot.refCount.Store(1)
    
    // Apply file changes
    for path, file := range s.diskFiles {
        newSnapshot.diskFiles[path] = file
    }
    
    return newSnapshot
}'''
    
    create_code_snippet(code, GoLexer(), 
                       "Snapshot System with Reference Counting", 
                       "snapshot.go")

def create_file_change_processing_example():
    """Create an example of file change processing"""
    code = '''// File change processing pipeline
func (s *Session) DidOpenFile(ctx context.Context, uri lsproto.DocumentUri, 
                             version int32, content string, 
                             languageKind lsproto.LanguageKind) {
    s.pendingFileChangesMu.Lock()
    s.pendingFileChanges = append(s.pendingFileChanges, FileChange{
        Kind:         FileChangeKindOpen,
        URI:          uri,
        Version:      version,
        Content:      content,
        LanguageKind: languageKind,
    })
    changes := s.flushChangesLocked(ctx)
    s.pendingFileChangesMu.Unlock()
    
    s.UpdateSnapshot(ctx, SnapshotChange{
        fileChanges:   changes,
        requestedURIs: []lsproto.DocumentUri{uri},
    })
}

func (s *Session) flushChangesLocked(ctx context.Context) FileChangeSummary {
    if len(s.pendingFileChanges) == 0 {
        return FileChangeSummary{}
    }
    
    start := time.Now()
    changes := s.fs.processChanges(s.pendingFileChanges)
    if s.options.LoggingEnabled {
        s.logger.Log(fmt.Sprintf("Processed %d file changes in %v", 
                                len(s.pendingFileChanges), time.Since(start)))
    }
    s.pendingFileChanges = nil
    return changes
}'''
    
    create_code_snippet(code, GoLexer(), 
                       "File Change Processing Pipeline", 
                       "file_changes.go")

def create_lsp_handler_example():
    """Create an example of LSP request handling"""
    code = '''// LSP request handler example
func (s *Server) handleCompletion(ctx context.Context, 
                                 req *lsproto.RequestMessage) error {
    params := req.Params.(*lsproto.CompletionParams)
    project := s.projectService.EnsureDefaultProjectForURI(params.TextDocument.Uri)
    
    languageService, done := project.GetLanguageServiceForRequest(ctx)
    defer done()
    
    // Panic recovery for gradual rollout
    defer func() {
        if r := recover(); r != nil {
            stack := debug.Stack()
            s.Log("panic obtaining completions:", r, string(stack))
            s.sendResult(req.ID, &lsproto.CompletionList{})
        }
    }()
    
    list, err := languageService.ProvideCompletion(
        ctx,
        params.TextDocument.Uri,
        params.Position,
        params.Context,
        getCompletionClientCapabilities(s.initializeParams),
        &ls.UserPreferences{})
    
    if err != nil {
        return err
    }
    
    s.sendResult(req.ID, list)
    return nil
}'''
    
    create_code_snippet(code, GoLexer(), 
                       "LSP Request Handler with Error Recovery", 
                       "lsp_handler.go")

def create_concurrent_processing_example():
    """Create an example of concurrent processing"""
    code = '''// Background task processing with goroutines
type BackgroundQueue struct {
    tasks   chan func(context.Context)
    workers int
    wg      sync.WaitGroup
    done    chan struct{}
}

func (bq *BackgroundQueue) Enqueue(ctx context.Context, task func(context.Context)) {
    select {
    case bq.tasks <- task:
    case <-ctx.Done():
        return
    case <-bq.done:
        return
    }
}

func (bq *BackgroundQueue) worker(ctx context.Context) {
    defer bq.wg.Done()
    for {
        select {
        case task := <-bq.tasks:
            func() {
                defer func() {
                    if r := recover(); r != nil {
                        // Log panic but don't crash worker
                        log.Printf("Background task panic: %v", r)
                    }
                }()
                task(ctx)
            }()
        case <-ctx.Done():
            return
        case <-bq.done:
            return
        }
    }
}

func (bq *BackgroundQueue) Start(ctx context.Context) {
    for i := 0; i < bq.workers; i++ {
        bq.wg.Add(1)
        go bq.worker(ctx)
    }
}'''
    
    create_code_snippet(code, GoLexer(), 
                       "Concurrent Background Task Processing", 
                       "background_queue.go")

def main():
    """Generate all code examples"""
    print("Generating syntax-highlighted code examples...")
    
    # Create output directory
    import os
    os.makedirs("code-examples", exist_ok=True)
    
    examples = [
        ("dirty.Map Usage", create_dirty_map_go_example),
        ("Snapshot System", create_snapshot_system_example),
        ("File Change Processing", create_file_change_processing_example),
        ("LSP Handler", create_lsp_handler_example),
        ("Concurrent Processing", create_concurrent_processing_example),
    ]
    
    for name, func in examples:
        print(f"  Creating {name}...")
        func()
        print(f"  ✓ {name} saved")
    
    print("\nCode examples generated successfully!")
    print("\nGenerated files in code-examples/:")
    print("  - project_collection_go.png")
    print("  - snapshot_go.png")
    print("  - file_changes_go.png")
    print("  - lsp_handler_go.png")
    print("  - background_queue_go.png")

if __name__ == "__main__":
    main()
