import React, { FormEvent } from "react";
import Button from "@components/Button";
import Input from "@components/Input";

export type LogInProps = {
  onSubmit?: (e: FormEvent) => void;
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