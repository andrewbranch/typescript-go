//// [tests/cases/compiler/errorRecoveryWithDotFollowedByNamespaceKeyword.ts] ////

//// [errorRecoveryWithDotFollowedByNamespaceKeyword.ts]
namespace A {
    function foo() {
        if (true) {
            B.
            

        namespace B {
            export function baz() { }
}

//// [errorRecoveryWithDotFollowedByNamespaceKeyword.js]
var A;
(function (A) {
    function foo() {
        if (true) {
            B.
            ;
            let B;
            (function (B) {
                function baz() { }
                B.baz = baz;
            })(B || (B = {}));
        }
    }
})(A || (A = {}));
