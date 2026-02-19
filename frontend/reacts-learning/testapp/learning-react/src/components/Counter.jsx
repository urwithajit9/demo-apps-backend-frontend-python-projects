import { useState } from "react";

export default function Counter() {
  const [count, setCount] = useState(0);
  function increment() {
    //console.log("hello");
    setCount(count + 1);
  }
  function decrement() {
    //console.log("hello");
    setCount(count - 1);
  }
  return (
    <div>
      <p>The Total count is:{count}</p>
      <button onClick={increment}>Increment</button>
      <button onClick={decrement}>Decrement</button>
    </div>
  );
}
