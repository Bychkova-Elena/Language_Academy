import React, { useCallback, useState } from "react";
import Input from "@components/Input";
import UserStore from "@store/UserStore";

const userStore = new UserStore();

const LogIn: React.FC = () => {

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = useCallback(
    (event) => {
      async () => {
      try {
        await userStore
          .LogIn({
          username: username,
          password: password
          })
        .then(result => {
          console.log(result);
        });
      } catch (err) {}
    };
    },
    []
  );
  
  return (
    <div>
    <form onSubmit={handleSubmit}>
      <label>
        Имя пользователя:
        <Input type="text" onChange={e => setUsername(e.target.value)} value={username} placeholder="Введите логин" />
      </label>
      <label>
        Пароль:
        <Input type="password" onChange={e => setPassword(e.target.value)} value={password} placeholder="Введите пароль" />
      </label>
      <Input type="submit" value="Отправить" />
      </form>
      </div>
  )
};

export default React.memo(LogIn);