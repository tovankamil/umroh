// src/services/authService.ts

import api from "@/services/api";

export interface LoginCredentials {
  username: string;
  password: string;
}

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

// Interface untuk data user lengkap
export interface UserData {
  user: {
    username: string;
    name: string | null;
    // phone_number: string;
    ktp: string;
    address: string;
    province: string;
    city: string;
    district: string;
    postal_code: string;
    level_status: string;
    sponsorships: any[];
    sponsorships_given: any[];
  };
  sponsorships_received_count: number;
  sponsorships_given_count: number;
  sponsorships_received: any[];
  sponsorships_given: any[];
}

export const login = async (
  credentials: LoginCredentials
): Promise<AuthResponse> => {
  // Untuk login, kita tidak menggunakan interceptor karena belum ada token
  const response = await api.post("/api/v1/login/", credentials);
  return response.data;
};

// Fungsi untuk mengambil data user
export const getUserData = async (username: string): Promise<UserData> => {
  try {
    const response = await api.get(`/api/v1/users/${username}`);
    console.log("User data response:", response.data);
    return response.data.data;
  } catch (error) {
    throw error;
  }
};

export const verifyToken = async (token: string): Promise<boolean> => {
  try {
    const response = await api.post("/api/v1/token/verify/", { token });
    console.log(response);
    return response.data.valid;
  } catch (error) {
    return false;
  }
};
