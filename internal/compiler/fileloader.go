package compiler

import (
	"cmp"
	"slices"
	"strings"
	"sync"
	"sync/atomic"

	"github.com/microsoft/typescript-go/internal/ast"
	"github.com/microsoft/typescript-go/internal/collections"
	"github.com/microsoft/typescript-go/internal/core"
	"github.com/microsoft/typescript-go/internal/module"
	"github.com/microsoft/typescript-go/internal/tsoptions"
	"github.com/microsoft/typescript-go/internal/tspath"
)

type fileLoader struct {
	opts                ProgramOptions
	resolver            *module.Resolver
	defaultLibraryPath  string
	comparePathsOptions tspath.ComparePathsOptions
	supportedExtensions []string

	parseTasks                 *fileLoaderWorker[*parseTask]
	projectReferenceParseTasks *fileLoaderWorker[*projectReferenceParseTask]
	rootTasks                  []*parseTask

	totalFileCount atomic.Int32
	libFileCount   atomic.Int32

	factoryMu sync.Mutex
	factory   ast.NodeFactory

	projectReferenceFileMapper *projectReferenceFileMapper
	dtsDirectories             collections.Set[tspath.Path]
}

type processedFiles struct {
	resolver                      *module.Resolver
	files                         []*ast.SourceFile
	filesByPath                   map[tspath.Path]*ast.SourceFile
	projectReferenceFileMapper    *projectReferenceFileMapper
	missingFiles                  []string
	resolvedModules               map[tspath.Path]module.ModeAwareCache[*module.ResolvedModule]
	typeResolutionsInFile         map[tspath.Path]module.ModeAwareCache[*module.ResolvedTypeReferenceDirective]
	sourceFileMetaDatas           map[tspath.Path]*ast.SourceFileMetaData
	jsxRuntimeImportSpecifiers    map[tspath.Path]*jsxRuntimeImportSpecifier
	importHelpersImportSpecifiers map[tspath.Path]*ast.Node
	// List of present unsupported extensions
	unsupportedExtensions []string
}

type jsxRuntimeImportSpecifier struct {
	moduleReference string
	specifier       *ast.Node
}

func processAllProgramFiles(
	opts ProgramOptions,
	libs []string,
	singleThreaded bool,
) processedFiles {
	compilerOptions := opts.Config.CompilerOptions()
	rootFiles := opts.Config.FileNames()
	supportedExtensions := tsoptions.GetSupportedExtensions(compilerOptions, nil /*extraFileExtensions*/)
	loader := fileLoader{
		opts:               opts,
		defaultLibraryPath: tspath.GetNormalizedAbsolutePath(opts.Host.DefaultLibraryPath(), opts.Host.GetCurrentDirectory()),
		comparePathsOptions: tspath.ComparePathsOptions{
			UseCaseSensitiveFileNames: opts.Host.FS().UseCaseSensitiveFileNames(),
			CurrentDirectory:          opts.Host.GetCurrentDirectory(),
		},
		parseTasks: &fileLoaderWorker[*parseTask]{
			wg:          core.NewWorkGroup(singleThreaded),
			getSubTasks: getSubTasksOfParseTask,
		},
		projectReferenceParseTasks: &fileLoaderWorker[*projectReferenceParseTask]{
			wg:          core.NewWorkGroup(singleThreaded),
			getSubTasks: getSubTasksOfProjectReferenceParseTask,
		},
		rootTasks:           make([]*parseTask, 0, len(rootFiles)+len(libs)),
		supportedExtensions: core.Flatten(tsoptions.GetSupportedExtensionsWithJsonIfResolveJsonModule(compilerOptions, supportedExtensions)),
	}
	loader.addProjectReferenceTasks()
	loader.resolver = module.NewResolver(loader.projectReferenceFileMapper.host, compilerOptions, opts.TypingsLocation, opts.ProjectName)
	loader.addRootTasks(rootFiles, false)
	loader.addRootTasks(libs, true)
	loader.addAutomaticTypeDirectiveTasks()

	loader.parseTasks.runAndWait(&loader, loader.rootTasks)
	// Clear out loader and host to ensure its not used post program creation
	loader.projectReferenceFileMapper.loader = nil
	loader.projectReferenceFileMapper.host = nil

	totalFileCount := int(loader.totalFileCount.Load())
	libFileCount := int(loader.libFileCount.Load())

	var missingFiles []string
	files := make([]*ast.SourceFile, 0, totalFileCount-libFileCount)
	libFiles := make([]*ast.SourceFile, 0, totalFileCount) // totalFileCount here since we append files to it later to construct the final list

	filesByPath := make(map[tspath.Path]*ast.SourceFile, totalFileCount)
	resolvedModules := make(map[tspath.Path]module.ModeAwareCache[*module.ResolvedModule], totalFileCount)
	typeResolutionsInFile := make(map[tspath.Path]module.ModeAwareCache[*module.ResolvedTypeReferenceDirective], totalFileCount)
	sourceFileMetaDatas := make(map[tspath.Path]*ast.SourceFileMetaData, totalFileCount)
	var jsxRuntimeImportSpecifiers map[tspath.Path]*jsxRuntimeImportSpecifier
	var importHelpersImportSpecifiers map[tspath.Path]*ast.Node
	var unsupportedExtensions []string

	loader.parseTasks.collect(&loader, loader.rootTasks, func(task *parseTask, _ []tspath.Path) {
		file := task.file
		if task.isRedirected {
			return
		}
		if file == nil {
			missingFiles = append(missingFiles, task.normalizedFilePath)
			return
		}
		if task.isLib {
			libFiles = append(libFiles, file)
		} else {
			files = append(files, file)
		}
		path := file.Path()

		filesByPath[path] = file
		resolvedModules[path] = task.resolutionsInFile
		typeResolutionsInFile[path] = task.typeResolutionsInFile
		sourceFileMetaDatas[path] = task.metadata
		if task.jsxRuntimeImportSpecifier != nil {
			if jsxRuntimeImportSpecifiers == nil {
				jsxRuntimeImportSpecifiers = make(map[tspath.Path]*jsxRuntimeImportSpecifier, totalFileCount)
			}
			jsxRuntimeImportSpecifiers[path] = task.jsxRuntimeImportSpecifier
		}
		if task.importHelpersImportSpecifier != nil {
			if importHelpersImportSpecifiers == nil {
				importHelpersImportSpecifiers = make(map[tspath.Path]*ast.Node, totalFileCount)
			}
			importHelpersImportSpecifiers[path] = task.importHelpersImportSpecifier
		}
		extension := tspath.TryGetExtensionFromPath(file.FileName())
		if slices.Contains(tspath.SupportedJSExtensionsFlat, extension) {
			unsupportedExtensions = core.AppendIfUnique(unsupportedExtensions, extension)
		}
	})
	loader.sortLibs(libFiles)

	allFiles := append(libFiles, files...)

	return processedFiles{
		resolver:                      loader.resolver,
		files:                         allFiles,
		filesByPath:                   filesByPath,
		projectReferenceFileMapper:    loader.projectReferenceFileMapper,
		resolvedModules:               resolvedModules,
		typeResolutionsInFile:         typeResolutionsInFile,
		sourceFileMetaDatas:           sourceFileMetaDatas,
		jsxRuntimeImportSpecifiers:    jsxRuntimeImportSpecifiers,
		importHelpersImportSpecifiers: importHelpersImportSpecifiers,
		unsupportedExtensions:         unsupportedExtensions,
	}
}

func (p *fileLoader) toPath(file string) tspath.Path {
	return tspath.ToPath(file, p.opts.Host.GetCurrentDirectory(), p.opts.Host.FS().UseCaseSensitiveFileNames())
}

func (p *fileLoader) addRootTasks(files []string, isLib bool) {
	for _, fileName := range files {
		absPath := tspath.GetNormalizedAbsolutePath(fileName, p.opts.Host.GetCurrentDirectory())
		if core.Tristate.IsTrue(p.opts.Config.CompilerOptions().AllowNonTsExtensions) || slices.Contains(p.supportedExtensions, tspath.TryGetExtensionFromPath(absPath)) {
			p.rootTasks = append(p.rootTasks, &parseTask{normalizedFilePath: absPath, isLib: isLib})
		}
	}
}

func (p *fileLoader) addAutomaticTypeDirectiveTasks() {
	var containingDirectory string
	compilerOptions := p.opts.Config.CompilerOptions()
	if compilerOptions.ConfigFilePath != "" {
		containingDirectory = tspath.GetDirectoryPath(compilerOptions.ConfigFilePath)
	} else {
		containingDirectory = p.opts.Host.GetCurrentDirectory()
	}
	containingFileName := tspath.CombinePaths(containingDirectory, module.InferredTypesContainingFile)

	automaticTypeDirectiveNames := module.GetAutomaticTypeDirectiveNames(compilerOptions, p.opts.Host)
	for _, name := range automaticTypeDirectiveNames {
		resolved := p.resolver.ResolveTypeReferenceDirective(name, containingFileName, core.ModuleKindNodeNext, nil)
		if resolved.IsResolved() {
			p.rootTasks = append(p.rootTasks, &parseTask{normalizedFilePath: resolved.ResolvedFileName, isLib: false})
		}
	}
}

func (p *fileLoader) addProjectReferenceTasks() {
	p.projectReferenceFileMapper = &projectReferenceFileMapper{
		opts: p.opts,
		host: p.opts.Host,
	}
	projectReferences := p.opts.Config.ResolvedProjectReferencePaths()
	if len(projectReferences) == 0 {
		return
	}

	rootTasks := createProjectReferenceParseTasks(projectReferences)
	p.projectReferenceParseTasks.runAndWait(p, rootTasks)
	p.projectReferenceFileMapper.init(p, rootTasks)

	// Add files from project references as root if the module kind is 'none'.
	// This ensures that files from project references are included in the root tasks
	// when no module system is specified, allowing including all files for global symbol merging
	// !!! sheetal Do we really need it?
	if len(p.opts.Config.FileNames()) != 0 {
		for _, resolved := range p.projectReferenceFileMapper.getResolvedProjectReferences() {
			if resolved == nil || resolved.CompilerOptions().GetEmitModuleKind() != core.ModuleKindNone {
				continue
			}
			if p.opts.canUseProjectReferenceSource() {
				for _, fileName := range resolved.FileNames() {
					p.rootTasks = append(p.rootTasks, &parseTask{normalizedFilePath: fileName, isLib: false})
				}
			} else {
				for outputDts := range resolved.GetOutputDeclarationFileNames() {
					if outputDts != "" {
						p.rootTasks = append(p.rootTasks, &parseTask{normalizedFilePath: outputDts, isLib: false})
					}
				}
			}
		}
	}
}

func (p *fileLoader) sortLibs(libFiles []*ast.SourceFile) {
	slices.SortFunc(libFiles, func(f1 *ast.SourceFile, f2 *ast.SourceFile) int {
		return cmp.Compare(p.getDefaultLibFilePriority(f1), p.getDefaultLibFilePriority(f2))
	})
}

func (p *fileLoader) getDefaultLibFilePriority(a *ast.SourceFile) int {
	// defaultLibraryPath and a.FileName() are absolute and normalized; a prefix check should suffice.
	defaultLibraryPath := tspath.RemoveTrailingDirectorySeparator(p.defaultLibraryPath)
	aFileName := a.FileName()

	if strings.HasPrefix(aFileName, defaultLibraryPath) && len(aFileName) > len(defaultLibraryPath) && aFileName[len(defaultLibraryPath)] == tspath.DirectorySeparator {
		// avoid tspath.GetBaseFileName; we know these paths are already absolute and normalized.
		basename := aFileName[strings.LastIndexByte(aFileName, tspath.DirectorySeparator)+1:]
		if basename == "lib.d.ts" || basename == "lib.es6.d.ts" {
			return 0
		}
		name := strings.TrimSuffix(strings.TrimPrefix(basename, "lib."), ".d.ts")
		index := slices.Index(tsoptions.Libs, name)
		if index != -1 {
			return index + 1
		}
	}
	return len(tsoptions.Libs) + 2
}

func (p *fileLoader) loadSourceFileMetaData(fileName string) *ast.SourceFileMetaData {
	packageJsonScope := p.resolver.GetPackageJsonScopeIfApplicable(fileName)
	var packageJsonType, packageJsonDirectory string
	if packageJsonScope.Exists() {
		packageJsonDirectory = packageJsonScope.PackageDirectory
		if value, ok := packageJsonScope.Contents.Type.GetValue(); ok {
			packageJsonType = value
		}
	}
	impliedNodeFormat := ast.GetImpliedNodeFormatForFile(fileName, packageJsonType)
	return &ast.SourceFileMetaData{
		PackageJsonType:      packageJsonType,
		PackageJsonDirectory: packageJsonDirectory,
		ImpliedNodeFormat:    impliedNodeFormat,
	}
}

func (p *fileLoader) parseSourceFile(t *parseTask) *ast.SourceFile {
	path := p.toPath(t.normalizedFilePath)
	sourceFile := p.opts.Host.GetSourceFile(t.normalizedFilePath, path, p.projectReferenceFileMapper.getCompilerOptionsForFile(t).SourceFileAffecting(), t.metadata)
	return sourceFile
}

func (p *fileLoader) resolveTripleslashPathReference(moduleName string, containingFile string) string {
	basePath := tspath.GetDirectoryPath(containingFile)
	referencedFileName := moduleName

	if !tspath.IsRootedDiskPath(moduleName) {
		referencedFileName = tspath.CombinePaths(basePath, moduleName)
	}
	return tspath.NormalizePath(referencedFileName)
}

func (p *fileLoader) resolveTypeReferenceDirectives(file *ast.SourceFile, meta *ast.SourceFileMetaData) (
	toParse []string,
	typeResolutionsInFile module.ModeAwareCache[*module.ResolvedTypeReferenceDirective],
) {
	if len(file.TypeReferenceDirectives) != 0 {
		toParse = make([]string, 0, len(file.TypeReferenceDirectives))
		typeResolutionsInFile = make(module.ModeAwareCache[*module.ResolvedTypeReferenceDirective], len(file.TypeReferenceDirectives))
		for _, ref := range file.TypeReferenceDirectives {
			redirect := p.projectReferenceFileMapper.getRedirectForResolution(file)
			resolutionMode := getModeForTypeReferenceDirectiveInFile(ref, file, meta, module.GetCompilerOptionsWithRedirect(p.opts.Config.CompilerOptions(), redirect))
			resolved := p.resolver.ResolveTypeReferenceDirective(ref.FileName, file.FileName(), resolutionMode, redirect)
			typeResolutionsInFile[module.ModeAwareCacheKey{Name: ref.FileName, Mode: resolutionMode}] = resolved
			if resolved.IsResolved() {
				toParse = append(toParse, resolved.ResolvedFileName)
			}
		}
	}
	return toParse, typeResolutionsInFile
}

const externalHelpersModuleNameText = "tslib" // TODO(jakebailey): dedupe

func (p *fileLoader) resolveImportsAndModuleAugmentations(file *ast.SourceFile, meta *ast.SourceFileMetaData) (
	toParse []string,
	resolutionsInFile module.ModeAwareCache[*module.ResolvedModule],
	importHelpersImportSpecifier *ast.Node,
	jsxRuntimeImportSpecifier_ *jsxRuntimeImportSpecifier,
) {
	moduleNames := make([]*ast.Node, 0, len(file.Imports())+len(file.ModuleAugmentations)+2)
	moduleNames = append(moduleNames, file.Imports()...)
	for _, imp := range file.ModuleAugmentations {
		if imp.Kind == ast.KindStringLiteral {
			moduleNames = append(moduleNames, imp)
		}
		// Do nothing if it's an Identifier; we don't need to do module resolution for `declare global`.
	}

	isJavaScriptFile := ast.IsSourceFileJS(file)
	isExternalModuleFile := ast.IsExternalModule(file)

	redirect := p.projectReferenceFileMapper.getRedirectForResolution(file)
	optionsForFile := module.GetCompilerOptionsWithRedirect(p.opts.Config.CompilerOptions(), redirect)
	if isJavaScriptFile || (!file.IsDeclarationFile && (optionsForFile.GetIsolatedModules() || isExternalModuleFile)) {
		if optionsForFile.ImportHelpers.IsTrue() {
			specifier := p.createSyntheticImport(externalHelpersModuleNameText, file)
			moduleNames = append(moduleNames, specifier)
			importHelpersImportSpecifier = specifier
		}

		jsxImport := ast.GetJSXRuntimeImport(ast.GetJSXImplicitImportBase(optionsForFile, file), optionsForFile)
		if jsxImport != "" {
			specifier := p.createSyntheticImport(jsxImport, file)
			moduleNames = append(moduleNames, specifier)
			jsxRuntimeImportSpecifier_ = &jsxRuntimeImportSpecifier{
				moduleReference: jsxImport,
				specifier:       specifier,
			}
		}
	}

	if len(moduleNames) != 0 {
		toParse = make([]string, 0, len(moduleNames))

		resolutions := p.resolveModuleNames(moduleNames, file, meta, redirect)

		resolutionsInFile = make(module.ModeAwareCache[*module.ResolvedModule], len(resolutions))

		for _, resolution := range resolutions {
			resolvedFileName := resolution.resolvedModule.ResolvedFileName
			// TODO(ercornel): !!!: check if from node modules

			mode := getModeForUsageLocation(file.FileName(), meta, resolution.node, optionsForFile)
			resolutionsInFile[module.ModeAwareCacheKey{Name: resolution.node.Text(), Mode: mode}] = resolution.resolvedModule

			// add file to program only if:
			// - resolution was successful
			// - noResolve is falsy
			// - module name comes from the list of imports
			// - it's not a top level JavaScript module that exceeded the search max

			// const elideImport = isJSFileFromNodeModules && currentNodeModulesDepth > maxNodeModuleJsDepth;

			// Don't add the file if it has a bad extension (e.g. 'tsx' if we don't have '--allowJs')
			// This may still end up being an untyped module -- the file won't be included but imports will be allowed.
			hasAllowedExtension := false
			if optionsForFile.GetResolveJsonModule() {
				hasAllowedExtension = tspath.FileExtensionIsOneOf(resolvedFileName, tspath.SupportedTSExtensionsWithJsonFlat)
			} else if optionsForFile.AllowJs.IsTrue() {
				hasAllowedExtension = tspath.FileExtensionIsOneOf(resolvedFileName, tspath.SupportedJSExtensionsFlat) || tspath.FileExtensionIsOneOf(resolvedFileName, tspath.SupportedTSExtensionsFlat)
			} else {
				hasAllowedExtension = tspath.FileExtensionIsOneOf(resolvedFileName, tspath.SupportedTSExtensionsFlat)
			}
			shouldAddFile := resolution.resolvedModule.IsResolved() && hasAllowedExtension
			// TODO(ercornel): !!!: other checks on whether or not to add the file

			if shouldAddFile {
				// p.findSourceFile(resolvedFileName, FileIncludeReason{Import, 0})
				toParse = append(toParse, resolvedFileName)
			}
		}
	}

	return toParse, resolutionsInFile, importHelpersImportSpecifier, jsxRuntimeImportSpecifier_
}

func (p *fileLoader) resolveModuleNames(entries []*ast.Node, file *ast.SourceFile, meta *ast.SourceFileMetaData, redirect *tsoptions.ParsedCommandLine) []*resolution {
	if len(entries) == 0 {
		return nil
	}

	resolvedModules := make([]*resolution, 0, len(entries))

	for _, entry := range entries {
		moduleName := entry.Text()
		if moduleName == "" {
			continue
		}
		resolvedModule := p.resolver.ResolveModuleName(moduleName, file.FileName(), getModeForUsageLocation(file.FileName(), meta, entry, module.GetCompilerOptionsWithRedirect(p.opts.Config.CompilerOptions(), redirect)), redirect)
		resolvedModules = append(resolvedModules, &resolution{node: entry, resolvedModule: resolvedModule})
	}

	return resolvedModules
}

func (p *fileLoader) createSyntheticImport(text string, file *ast.SourceFile) *ast.Node {
	p.factoryMu.Lock()
	defer p.factoryMu.Unlock()
	externalHelpersModuleReference := p.factory.NewStringLiteral(text)
	importDecl := p.factory.NewImportDeclaration(nil, nil, externalHelpersModuleReference, nil)
	// !!! addInternalEmitFlags(importDecl, InternalEmitFlags.NeverApplyImportHelper);
	externalHelpersModuleReference.Parent = importDecl
	importDecl.Parent = file.AsNode()
	// !!! externalHelpersModuleReference.Flags &^= ast.NodeFlagsSynthesized
	// !!! importDecl.Flags &^= ast.NodeFlagsSynthesized
	return externalHelpersModuleReference
}

type resolution struct {
	node           *ast.Node
	resolvedModule *module.ResolvedModule
}

func getModeForTypeReferenceDirectiveInFile(ref *ast.FileReference, file *ast.SourceFile, meta *ast.SourceFileMetaData, options *core.CompilerOptions) core.ResolutionMode {
	if ref.ResolutionMode != core.ResolutionModeNone {
		return ref.ResolutionMode
	} else {
		return getDefaultResolutionModeForFile(file.FileName(), meta, options)
	}
}

func getDefaultResolutionModeForFile(fileName string, meta *ast.SourceFileMetaData, options *core.CompilerOptions) core.ResolutionMode {
	if importSyntaxAffectsModuleResolution(options) {
		return ast.GetImpliedNodeFormatForEmitWorker(fileName, options.GetEmitModuleKind(), meta)
	} else {
		return core.ResolutionModeNone
	}
}

func getModeForUsageLocation(fileName string, meta *ast.SourceFileMetaData, usage *ast.StringLiteralLike, options *core.CompilerOptions) core.ResolutionMode {
	if ast.IsImportDeclaration(usage.Parent) || ast.IsExportDeclaration(usage.Parent) || ast.IsJSDocImportTag(usage.Parent) {
		isTypeOnly := ast.IsExclusivelyTypeOnlyImportOrExport(usage.Parent)
		if isTypeOnly {
			var override core.ResolutionMode
			var ok bool
			switch usage.Parent.Kind {
			case ast.KindImportDeclaration:
				override, ok = usage.Parent.AsImportDeclaration().Attributes.GetResolutionModeOverride()
			case ast.KindExportDeclaration:
				override, ok = usage.Parent.AsExportDeclaration().Attributes.GetResolutionModeOverride()
			case ast.KindJSDocImportTag:
				override, ok = usage.Parent.AsJSDocImportTag().Attributes.GetResolutionModeOverride()
			}
			if ok {
				return override
			}
		}
	}
	if ast.IsLiteralTypeNode(usage.Parent) && ast.IsImportTypeNode(usage.Parent.Parent) {
		if override, ok := usage.Parent.Parent.AsImportTypeNode().Attributes.GetResolutionModeOverride(); ok {
			return override
		}
	}

	if options != nil && importSyntaxAffectsModuleResolution(options) {
		return getEmitSyntaxForUsageLocationWorker(fileName, meta, usage, options)
	}

	return core.ResolutionModeNone
}

func importSyntaxAffectsModuleResolution(options *core.CompilerOptions) bool {
	moduleResolution := options.GetModuleResolutionKind()
	return core.ModuleResolutionKindNode16 <= moduleResolution && moduleResolution <= core.ModuleResolutionKindNodeNext ||
		options.GetResolvePackageJsonExports() || options.GetResolvePackageJsonImports()
}

func getEmitSyntaxForUsageLocationWorker(fileName string, meta *ast.SourceFileMetaData, usage *ast.Node, options *core.CompilerOptions) core.ResolutionMode {
	if ast.IsRequireCall(usage.Parent) || ast.IsExternalModuleReference(usage.Parent) && ast.IsImportEqualsDeclaration(usage.Parent.Parent) {
		return core.ModuleKindCommonJS
	}
	fileEmitMode := ast.GetEmitModuleFormatOfFileWorker(fileName, options, meta)
	if ast.IsImportCall(ast.WalkUpParenthesizedExpressions(usage.Parent)) {
		if ast.ShouldTransformImportCall(fileName, options, fileEmitMode) {
			return core.ModuleKindCommonJS
		} else {
			return core.ModuleKindESNext
		}
	}
	// If we're in --module preserve on an input file, we know that an import
	// is an import. But if this is a declaration file, we'd prefer to use the
	// impliedNodeFormat. Since we want things to be consistent between the two,
	// we need to issue errors when the user writes ESM syntax in a definitely-CJS
	// file, until/unless declaration emit can indicate a true ESM import. On the
	// other hand, writing CJS syntax in a definitely-ESM file is fine, since declaration
	// emit preserves the CJS syntax.
	if fileEmitMode == core.ModuleKindCommonJS {
		return core.ModuleKindCommonJS
	} else {
		if fileEmitMode.IsNonNodeESM() || fileEmitMode == core.ModuleKindPreserve {
			return core.ModuleKindESNext
		}
	}
	return core.ModuleKindNone
}
