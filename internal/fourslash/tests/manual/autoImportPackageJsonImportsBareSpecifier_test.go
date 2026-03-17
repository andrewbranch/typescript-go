package fourslash_test

import (
	"testing"

	"github.com/microsoft/typescript-go/internal/fourslash"
	"github.com/microsoft/typescript-go/internal/testutil"
)

func TestAutoImportPackageJsonImportsBareSpecifier(t *testing.T) {
	t.Parallel()
	defer testutil.RecoverAndFail(t, "Panic on fourslash test")
	const content = `// @module: node18
// @Filename: /node_modules/pkg2/package.json
{
  "name": "pkg2",
  "version": "1.0.0",
  "exports": {
    "./*": "./src/*"
  }
}
// @Filename: /node_modules/pkg2/src/testing.ts
export function testing(): any;
// @Filename: /package.json
{
  "dependencies": {
    "pkg2": "*"
  },
  "imports": {
    "#pkg2/*": "pkg2/src/*"
  }
}
// @Filename: /a.ts
testing/**/`
	f, done := fourslash.NewFourslash(t, nil /*capabilities*/, content)
	defer done()
	f.VerifyImportFixModuleSpecifiers(t, "", []string{"#pkg2/testing.js"}, nil /*preferences*/)
}
