package fourslash_test

import (
	"testing"

	"github.com/microsoft/typescript-go/internal/fourslash"
	"github.com/microsoft/typescript-go/internal/testutil"
)

func TestAutoImportPackageJsonImportsBareSpecifierExact(t *testing.T) {
	t.Parallel()
	defer testutil.RecoverAndFail(t, "Panic on fourslash test")
	const content = `// @module: node18
// @Filename: /node_modules/pkg2/package.json
{
  "name": "pkg2",
  "version": "1.0.0",
  "exports": {
    "./testing": "./src/testing.ts"
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
    "#test": "pkg2/src/testing.ts"
  }
}
// @Filename: /a.ts
testing/**/`
	f, done := fourslash.NewFourslash(t, nil /*capabilities*/, content)
	defer done()
	f.VerifyImportFixModuleSpecifiers(t, "", []string{"#test"}, nil /*preferences*/)
}
