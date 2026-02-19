const greeting: string = "Hello, TypeScript! with watch";
let text = "Hello world!";
// Hover over "text", you'll see: let text: string
type Person = string;
const myName: Person = "Ajit Kumar";
console.log(greeting + myName);

function printMessage(message: any) {
  if (typeof message === "string") {
    // If the value is a string, print the message in uppercase.
    console.log("Message is: " + message.toUpperCase());
  } else {
    // If the value is not a string, alert the user.
    console.log("Provided value is not a string.");
  }
}

printMessage("Hello!"); // Output: Message is: HELLO!
printMessage(123);

type Status = "active" | "inactive" | "pending";

const getStatusMessage = (status: Status) => {
  console.log("The status is " + status);
};

getStatusMessage("active");

type ValueType = number | string;
const processValue = (value: ValueType) => {
  if (typeof value === "string") console.log(value.length);
  else {
    console.log(value * value);
  }
};

processValue("ajit");
processValue(5);

const handleUnknown = (value: unknown) => {
  if (typeof value === "number") return value * value;
  else if (typeof value === "string") {
    return value.toUpperCase();
  } else {
    return "Unsupported type";
  }
};

console.log(handleUnknown("ajit"));
console.log(handleUnknown(5));
console.log(handleUnknown(5.0));

let numberArray: Array<number> = [10, 20, 30];

interface User {
  id: number;
  name: string;
  email: string;
}

// simple users array
const users: User[] = [
  { id: 1, name: "John Doe", email: "john@example.com" },
  { id: 2, name: "Jane Smith", email: "jane@example.com" },
];

const numbers = [1, 2, 3, 4, 5];

numbers.forEach((number) => {
  console.log(number);
});

const squared = numbers.map((number) => number * number);
console.log(squared);

const evensquared = numbers
  .map((number) => number * number)
  .filter((number) => number % 2 == 0);

let ages = [18, 25, 30];
ages.push(40);

let ages2: number[];
ages2.push(18);
ages2.push(25);
