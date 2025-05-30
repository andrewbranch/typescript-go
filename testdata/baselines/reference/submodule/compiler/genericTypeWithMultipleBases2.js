//// [tests/cases/compiler/genericTypeWithMultipleBases2.ts] ////

//// [genericTypeWithMultipleBases2.ts]
export interface I1 {
    m1: () => void;
}
 
export interface I2 {
    m2: () => void;
}
 
export interface I3<T> extends I2, I1 {
    p1: T;
}
 
var x: I3<number>;
x.p1;
x.m1();
x.m2();



//// [genericTypeWithMultipleBases2.js]
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var x;
x.p1;
x.m1();
x.m2();
