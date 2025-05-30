//// [tests/cases/conformance/types/thisType/fluentClasses.ts] ////

//// [fluentClasses.ts]
class A {
    foo() {
        return this;
    }
}
class B extends A {
    bar() {
        return this;
    }
}
class C extends B {
    baz() {
        return this;
    }
}
var c: C;
var z = c.foo().bar().baz();  // Fluent pattern


//// [fluentClasses.js]
class A {
    foo() {
        return this;
    }
}
class B extends A {
    bar() {
        return this;
    }
}
class C extends B {
    baz() {
        return this;
    }
}
var c;
var z = c.foo().bar().baz(); // Fluent pattern
