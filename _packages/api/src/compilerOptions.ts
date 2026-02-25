import type { JsxEmit } from "#enums/jsxEmit";
import type { ModuleDetectionKind } from "#enums/moduleDetectionKind";
import type { ModuleKind } from "#enums/moduleKind";
import type { ModuleResolutionKind } from "#enums/moduleResolutionKind";
import type { NewLineKind } from "#enums/newLineKind";
import type { ScriptTarget } from "#enums/scriptTarget";

export type { JsxEmit, ModuleDetectionKind, ModuleKind, ModuleResolutionKind, NewLineKind, ScriptTarget };

/**
 * Compiler options as configured in tsconfig.json.
 *
 * Fields not set in tsconfig.json are absent (undefined).
 * Use `resolvedCompilerOptions` on ProjectResponse to get computed values.
 */
export interface CompilerOptions {
    allowJs?: boolean;
    allowArbitraryExtensions?: boolean;
    allowSyntheticDefaultImports?: boolean;
    allowImportingTsExtensions?: boolean;
    allowNonTsExtensions?: boolean;
    allowUmdGlobalAccess?: boolean;
    allowUnreachableCode?: boolean;
    allowUnusedLabels?: boolean;
    assumeChangesOnlyAffectDirectDependencies?: boolean;
    checkJs?: boolean;
    customConditions?: string[];
    composite?: boolean;
    emitDeclarationOnly?: boolean;
    emitBOM?: boolean;
    emitDecoratorMetadata?: boolean;
    downlevelIteration?: boolean;
    declaration?: boolean;
    declarationDir?: string;
    declarationMap?: boolean;
    deduplicatePackages?: boolean;
    disableSizeLimit?: boolean;
    disableSourceOfProjectReferenceRedirect?: boolean;
    disableSolutionSearching?: boolean;
    disableReferencedProjectLoad?: boolean;
    erasableSyntaxOnly?: boolean;
    esModuleInterop?: boolean;
    exactOptionalPropertyTypes?: boolean;
    experimentalDecorators?: boolean;
    forceConsistentCasingInFileNames?: boolean;
    isolatedModules?: boolean;
    isolatedDeclarations?: boolean;
    ignoreDeprecations?: string;
    importHelpers?: boolean;
    inlineSourceMap?: boolean;
    inlineSources?: boolean;
    incremental?: boolean;
    jsx?: JsxEmit;
    jsxFactory?: string;
    jsxFragmentFactory?: string;
    jsxImportSource?: string;
    lib?: string[];
    libReplacement?: boolean;
    locale?: string;
    mapRoot?: string;
    module?: ModuleKind;
    moduleResolution?: ModuleResolutionKind;
    moduleSuffixes?: string[];
    moduleDetection?: ModuleDetectionKind;
    newLine?: NewLineKind;
    noEmit?: boolean;
    noCheck?: boolean;
    noErrorTruncation?: boolean;
    noFallthroughCasesInSwitch?: boolean;
    noImplicitAny?: boolean;
    noImplicitThis?: boolean;
    noImplicitReturns?: boolean;
    noEmitHelpers?: boolean;
    noLib?: boolean;
    noPropertyAccessFromIndexSignature?: boolean;
    noUncheckedIndexedAccess?: boolean;
    noEmitOnError?: boolean;
    noUnusedLocals?: boolean;
    noUnusedParameters?: boolean;
    noResolve?: boolean;
    noImplicitOverride?: boolean;
    noUncheckedSideEffectImports?: boolean;
    outDir?: string;
    paths?: Record<string, string[]>;
    preserveConstEnums?: boolean;
    preserveSymlinks?: boolean;
    project?: string;
    resolveJsonModule?: boolean;
    resolvePackageJsonExports?: boolean;
    resolvePackageJsonImports?: boolean;
    removeComments?: boolean;
    rewriteRelativeImportExtensions?: boolean;
    reactNamespace?: string;
    rootDir?: string;
    rootDirs?: string[];
    skipLibCheck?: boolean;
    stableTypeOrdering?: boolean;
    strict?: boolean;
    strictBindCallApply?: boolean;
    strictBuiltinIteratorReturn?: boolean;
    strictFunctionTypes?: boolean;
    strictNullChecks?: boolean;
    strictPropertyInitialization?: boolean;
    stripInternal?: boolean;
    skipDefaultLibCheck?: boolean;
    sourceMap?: boolean;
    sourceRoot?: string;
    suppressOutputPathCheck?: boolean;
    target?: ScriptTarget;
    traceResolution?: boolean;
    tsBuildInfoFile?: string;
    typeRoots?: string[];
    types?: string[];
    useDefineForClassFields?: boolean;
    useUnknownInCatchVariables?: boolean;
    verbatimModuleSyntax?: boolean;
    maxNodeModuleJsDepth?: number;
}

/**
 * Resolved compiler options — computed option getters have been evaluated.
 *
 * This is a partial CompilerOptions containing only the fields whose effective
 * value differs from what is explicitly configured (e.g. `module` defaults to
 * `CommonJS` when `target` is ES5 and `module` is unset).
 */
export type ResolvedCompilerOptions = Partial<CompilerOptions>;
