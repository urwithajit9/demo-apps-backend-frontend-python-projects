"use client";
import { useFetch } from "@/hooks/useFetch";

export default function UsersList() {
  const {
    data: users,
    loading,
    error,
  } = useFetch<{ id: number; name: string }[]>(
    "https://jsonplaceholder.typicode.com/users"
  );

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <ul className="p-4 border bg-red-300 rounded-md">
      {users?.map((user) => (
        <li key={user.id} className="p-2 border-b">
          {user.name}
        </li>
      ))}
    </ul>
  );
}
