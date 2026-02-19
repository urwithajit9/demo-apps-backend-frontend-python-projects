"use client";
import CounterComponent from "@/components/Counter";
import UsersList from "@/components/UserList";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen py-2">
      <CounterComponent startWith={1} />
      <CounterComponent startWith={0} />
      <UsersList />
    </div>
  );
}
