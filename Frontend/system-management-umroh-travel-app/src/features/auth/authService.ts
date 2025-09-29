import axios from "axios";

// Menggunakan import.meta.env di Vite
const API_URL = import.meta.env.VITE_BACKEND_API_URL;

if (!API_URL) {
  throw new Error("BACKEND_API_URL environment variable is not defined");
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface AuthResponse {
  token: string;
  user: {
    id: string;
    username: string;
    name: string;
  };
}

export const login = async (
  credentials: LoginCredentials
): Promise<AuthResponse> => {
  const response = await axios.post(`${API_URL}/auth/login`, credentials);
  return response.data;
};
