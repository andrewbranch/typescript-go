//// [tests/cases/compiler/privacyCheckTypeOfFunction.ts] ////

//// [privacyCheckTypeOfFunction.ts]
function foo() {
}
export var x: typeof foo;
export var b = foo;


//// [privacyCheckTypeOfFunction.js]
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.b = exports.x = void 0;
function foo() {
}
exports.b = foo;
