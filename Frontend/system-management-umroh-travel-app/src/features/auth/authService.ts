import axios from "axios";

const API_URL = import.meta.env.VITE_BACKEND_API_URL;

if (!API_URL) {
  throw new Error("BACKEND_API_URL environment variable is not defined");
}

export interface LoginCredentials {
  username: string;
  password: string;
}

// Sesuaikan interface dengan respons backend
export interface AuthResponse {
  status: string;
  messages: string[];
  data: {
    access_token: string;
    refresh_token: string;
    user_id: string;
    username: string;
    email: string;
    level_status: string;
    name: string | null;
  };
}

export const login = async (
  credentials: LoginCredentials
): Promise<AuthResponse> => {
  const response = await axios.post(`${API_URL}api/v1/login/`, credentials);
  return response.data;
};
