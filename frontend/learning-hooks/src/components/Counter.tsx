"use client";
import { useCounter } from "@/hooks/useCounter";

export default function CounterComponent({ startWith }: { startWith: number }) {
  const { count, increment, decrement, reset } = useCounter(startWith); // Start from 5

  return (
    <div className="p-4 border rounded-md">
      <h2 className="text-lg font-bold">Counter: {count}</h2>
      <button onClick={increment} className="p-2 bg-green-500 text-white">
        +
      </button>
      <button onClick={decrement} className="p-2 bg-red-500 text-white">
        -
      </button>
      <button onClick={reset} className="p-2 bg-gray-500 text-white">
        Reset
      </button>
    </div>
  );
}
