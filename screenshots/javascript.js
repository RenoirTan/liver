// Fancy ES6 imports
import * as process from "process";
// Drab ES5 require
const readline = require("readline");

// Javascript Object
const stdio = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

// Function with promises
function userInput(string = "") {
// Fat arrow
    return new Promise((resolve, reject) => {
        stdio.question(string, (result) => {
            resolve(result);
        });
    });
}

// Class with unnecessary inheritance from Object
class Human extends Object {
    constructor(name) {
        this.name = name
    }

    /**
     * JSDoc example
     * 
     * @returns undefined
     */
    bark() {
        console.log("Meow")
    }
}

// Sausage
userInput("E")
    .then((answer) => {
        console.log(answer.charAt(Math.random() * answer.length));
// Keyword operators "new"
        var human = new Human(answer);
        human.bark();
    })
    .catch((err) => {
        console.err(err);
    });