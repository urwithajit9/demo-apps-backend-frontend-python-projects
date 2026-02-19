"use strict";
const greeting = "Hello, TypeScript! with watch";
let text = "Hello world!";
const myName = "Ajit Kumar";
console.log(greeting + myName);
function printMessage(message) {
    if (typeof message === "string") {
        // If the value is a string, print the message in uppercase.
        console.log("Message is: " + message.toUpperCase());
    }
    else {
        // If the value is not a string, alert the user.
        console.log("Provided value is not a string.");
    }
}
printMessage("Hello!"); // Output: Message is: HELLO!
printMessage(123);
const getStatusMessage = (status) => {
    console.log("The status is " + status);
};
getStatusMessage("active");
const processValue = (value) => {
    if (typeof value === "string")
        console.log(value.length);
    else {
        console.log(value * value);
    }
};
processValue("ajit");
processValue(5);
const handleUnknown = (value) => {
    if (typeof value === "number")
        return value * value;
    else if (typeof value === "string") {
        return value.toUpperCase();
    }
    else {
        return "Unsupported type";
    }
};
console.log(handleUnknown("ajit"));
console.log(handleUnknown(5));
console.log(handleUnknown(5.0));
