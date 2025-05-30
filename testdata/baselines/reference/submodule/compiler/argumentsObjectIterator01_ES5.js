//// [tests/cases/compiler/argumentsObjectIterator01_ES5.ts] ////

//// [argumentsObjectIterator01_ES5.ts]
function doubleAndReturnAsArray(x: number, y: number, z: number): [number, number, number] {
    let result = [];
    for (let arg of arguments) {
        result.push(arg + arg);
    }
    return <[any, any, any]>result;
}

//// [argumentsObjectIterator01_ES5.js]
function doubleAndReturnAsArray(x, y, z) {
    let result = [];
    for (let arg of arguments) {
        result.push(arg + arg);
    }
    return result;
}
