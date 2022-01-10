import React, { FormEvent } from "react";

import Input from "@components/Input";
import Button from "@components/Button";

export type LogInProps = {
  onSubmit: (e: FormEvent) => void;
};

const LogIn: React.FC<LogInProps> = ({  onSubmit= () => {}}) => (
  <form onSubmit={onSubmit}>
        <label>
          Имя пользователя:
          <Input value= "" placeholder="Введите пароль" />
    </label>
        <label>
          Пароль:
          <Input value= "" placeholder="Введите логин" />
        </label>
        <Button><input type="submit" value="Отправить" /></Button>
      </form>
);

export default React.memo(LogIn);