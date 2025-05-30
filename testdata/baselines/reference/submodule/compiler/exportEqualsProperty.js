//// [tests/cases/compiler/exportEqualsProperty.ts] ////

//// [declarations.d.ts]
declare namespace foo.bar {
    export type X = number;
    export const X: number;
}

declare module "foobar" {
    export = foo.bar;
}

declare module "foobarx" {
    export = foo.bar.X;
}

//// [a.ts]
namespace A {
    export class B { constructor(b: number) {} }
    export namespace B { export const b: number = 0; }
}
export = A.B;

//// [b.ts]
export = "foo".length;

//// [index.ts]
/// <reference path="declarations.d.ts" />
import { X } from "foobar";
import X2 = require("foobarx");
const x: X = X;
const x2: X2 = X2;

import B = require("./a");
const b: B = new B(B.b);

import fooLength = require("./b");
fooLength + 1;


//// [a.js]
"use strict";
var A;
(function (A) {
    class B {
        constructor(b) { }
    }
    A.B = B;
    (function (B) {
        B.b = 0;
    })(B = A.B || (A.B = {}));
})(A || (A = {}));
module.exports = A.B;
//// [b.js]
"use strict";
module.exports = "foo".length;
//// [index.js]
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
/// <reference path="declarations.d.ts" />
const foobar_1 = require("foobar");
const X2 = require("foobarx");
const x = foobar_1.X;
const x2 = X2;
const B = require("./a");
const b = new B(B.b);
const fooLength = require("./b");
fooLength + 1;
