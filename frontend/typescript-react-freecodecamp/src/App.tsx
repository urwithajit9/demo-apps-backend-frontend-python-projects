import { FC, useEffect, useState } from "react";
import axios from "axios";
import User from "./components/User";
import { AppProps, Users } from "./App.types";

//https://www.freecodecamp.org/news/use-typescript-with-react/

const App: FC<AppProps> = ({ title }) => {
  const [users, setUsers] = useState<Users[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [username, setUsername] = useState("");

  const handleChange = (event) => {
    setUsername(event.target.value);
  };

  const handleClick = async () => {
    try {
      setIsLoading(true);
      const { data } = await axios.get("https://randomuser.me/api/?results=10");
      console.log(data);
      setUsers(data.results);
    } catch (error) {
      console.log(error);
    } finally {
      setIsLoading(false);
    }
  };

  // useEffect(() => {
  //   const getUsers = async () => {

  //   };
  //   getUsers();
  // }, []);

  return (
    <div>
      <h1>{title}</h1>
      <button onClick={handleClick}>Show Users</button>

      <input type="text" onChange={handleChange} />
      {/* <input type="text" onChange={(event) => {}} /> */}
      <div>{username}</div>

      {isLoading && <p>Loading...</p>}

      <ul>
        {users.map(({ login, name, email }) => {
          return <User key={login.uuid} name={name} email={email} />;
        })}
      </ul>
    </div>
  );
};

export default App;
