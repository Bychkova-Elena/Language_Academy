import { ApiResponse } from "src/shared/store/ApiStore/types";

// Параметры запроса
export type LogInParams = {
  username: string;
  password: string;
};

export type UserItem = {
  username: string;
  email: string;
};

export interface IUserStore {
  LogIn(params: LogInParams): Promise<ApiResponse<UserItem, any>>;
}
