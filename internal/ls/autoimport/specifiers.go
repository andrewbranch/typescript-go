package autoimport

import (
	"strings"

	"github.com/microsoft/typescript-go/internal/modulespecifiers"
	"github.com/microsoft/typescript-go/internal/tspath"
)

func (v *View) GetModuleSpecifier(
	export *Export,
	userPreferences modulespecifiers.UserPreferences,
) (string, modulespecifiers.ResultKind) {
	// Ambient module
	if modulespecifiers.PathIsBareSpecifier(string(export.ModuleID)) {
		specifier := string(export.ModuleID)
		if modulespecifiers.IsExcludedByRegex(specifier, userPreferences.AutoImportSpecifierExcludeRegexes) {
			return "", modulespecifiers.ResultKindNone
		}
		return string(export.ModuleID), modulespecifiers.ResultKindAmbient
	}

	// For node_modules exports, check if a #-prefixed subpath import specifier
	// should be preferred. This is done before the entrypoint fast path so that
	// package.json "imports" entries take priority.
	if export.PackageName != "" {
		if v.getBareSpecifierImportPackages().Has(export.PackageName) {
			if specifier := v.tryGetSubpathImportSpecifier(export); specifier != "" {
				if !modulespecifiers.IsExcludedByRegex(specifier, userPreferences.AutoImportSpecifierExcludeRegexes) {
					return specifier, modulespecifiers.ResultKindNodeModules
				}
			}
		}

		if entrypoints, ok := v.registry.entrypoints[export.Path]; ok {
			for _, entrypoint := range entrypoints {
				if entrypoint.IncludeConditions.IsSubsetOf(v.conditions) && !v.conditions.Intersects(entrypoint.ExcludeConditions) {
					specifier := modulespecifiers.ProcessEntrypointEnding(
						entrypoint,
						userPreferences,
						v.program,
						v.program.Options(),
						v.importingFile,
						v.getAllowedEndings(),
					)

					if !modulespecifiers.IsExcludedByRegex(specifier, userPreferences.AutoImportSpecifierExcludeRegexes) {
						return specifier, modulespecifiers.ResultKindNodeModules
					}
				}
			}
			return "", modulespecifiers.ResultKindNone
		}
	}

	cache := v.registry.specifierCache[v.importingFile.Path()]
	if export.PackageName == "" {
		if specifier, ok := cache.Load(export.Path); ok {
			if specifier == "" {
				return "", modulespecifiers.ResultKindNone
			}
			return specifier, modulespecifiers.ResultKindRelative
		}
	}

	specifiers, kind := modulespecifiers.GetModuleSpecifiersForFileWithInfo(
		v.importingFile,
		export.ModuleFileName,
		v.program.Options(),
		v.program,
		userPreferences,
		modulespecifiers.ModuleSpecifierOptions{},
		true,
	)
	// !!! unsure when this could return multiple specifiers combined with the
	//     new node_modules code. Possibly with local symlinks, which should be
	//     very rare.
	for _, specifier := range specifiers {
		if strings.Contains(specifier, "/node_modules/") {
			continue
		}
		cache.Store(export.Path, specifier)
		return specifier, kind
	}
	cache.Store(export.Path, "")
	return "", modulespecifiers.ResultKindNone
}

// tryGetSubpathImportSpecifier attempts to generate a #-prefixed module specifier
// for a node_modules export using the importing file's package.json "imports" field.
func (v *View) tryGetSubpathImportSpecifier(export *Export) string {
	sourceDir := tspath.GetDirectoryPath(v.importingFile.FileName())
	importMode := v.program.GetDefaultResolutionModeForFile(v.importingFile)
	allowedEndings := v.getAllowedEndings()
	preferTsExtension := len(allowedEndings) > 0 && allowedEndings[0] == modulespecifiers.ModuleSpecifierEndingTsExtension

	return modulespecifiers.TryGetModuleNameFromPackageJsonImports(
		export.ModuleFileName,
		sourceDir,
		v.program.Options(),
		v.program,
		importMode,
		preferTsExtension,
	)
}
