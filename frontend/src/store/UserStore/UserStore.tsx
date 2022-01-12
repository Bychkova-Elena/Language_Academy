import ApiStore from "@shared/ApiStore";
import { ApiResponse, HTTPMethod } from "@shared/ApiStore/types";
import { IUserStore, LogInParams, UserItem } from "./types";

const BASE_URL: string = "api/auth";

export default class UserStore implements IUserStore {
  private readonly apiStore = new ApiStore(BASE_URL);

  async LogIn(params: LogInParams): Promise<ApiResponse<UserItem, any>> {
    return await this.apiStore.request({
      method: HTTPMethod.POST,
      endpoint: `/login`,
      headers: {},
      data: {}
    });
  }
}
