import React from "react";
import { ChangeEventHandler } from "react";


export type InputProps = {
  onChange?: ChangeEventHandler<HTMLInputElement>;
  value: string;
  placeholder?: string;
  type: string;
};

const Input: React.FC<InputProps> = ({ onChange, placeholder, value, type }) => (
  <input
    type={type }
    placeholder={placeholder}
    onChange={onChange}
    value={value}
  />
);

export default React.memo(Input);