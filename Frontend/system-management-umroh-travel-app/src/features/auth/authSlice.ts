// src/features/auth/authSlice.ts
import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import {
  getUserData,
  login,
  type LoginCredentials,
  type UserData,
} from "./authService";

interface User {
  id: string;
  username: string;
  name: string | null;
  email: string;
  level_status: string;
  phone_number?: string;
  ktp?: string;
  address?: string;
  province?: string;
  city?: string;
  district?: string;
  postal_code?: string;
}

interface AuthState {
  user: User | null;
  username: string | null;
  token: string | null;
  isLoading: boolean;
  error: string | null;
  userData: UserData | null;
  isUserDataLoading: boolean;
}

const initialState: AuthState = {
  user: null,
  username: localStorage.getItem("username"),
  token: localStorage.getItem("token"),
  isLoading: false,
  error: null,
  userData: null,
  isUserDataLoading: false,
};

export const loginUser = createAsyncThunk(
  "auth/loginUser",
  async (credentials: LoginCredentials, { rejectWithValue }) => {
    try {
      const response = await login(credentials);

      // Simpan access_token ke localStorage
      localStorage.setItem("token", response.data.access_token);
      localStorage.setItem("username", response.data.username);

      // Return data yang sudah diolah
      return {
        token: response.data.access_token,
        user: {
          id: response.data.user_id,
          username: response.data.username,
          name: response.data.name,
          email: response.data.email,
          level_status: response.data.level_status,
        },
      };
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || "Login failed");
    }
  }
);

// Async thunk untuk mengambil data user
export const fetchUserData = createAsyncThunk(
  "auth/fetchUserData",
  async (username: string, { rejectWithValue }) => {
    try {
      const userData = await getUserData(username);
      return userData;
    } catch (error: any) {
      return rejectWithValue(
        error.response?.data?.message || "Failed to fetch user data"
      );
    }
  }
);

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    logout: (state) => {
      state.user = null;
      state.username = null;
      state.token = null;
      state.userData = null;
      localStorage.removeItem("token");
      localStorage.removeItem("username"); // Tambahkan ini
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(loginUser.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(loginUser.fulfilled, (state, action) => {
        state.isLoading = false;
        state.user = action.payload.user;
        state.username = action.payload.user.username;
        state.token = action.payload.token;
      })
      .addCase(loginUser.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      .addCase(fetchUserData.pending, (state) => {
        state.isUserDataLoading = true;
        state.error = null;
      })
      .addCase(fetchUserData.fulfilled, (state, action) => {
        state.isUserDataLoading = false;
        state.userData = action.payload;
      })
      .addCase(fetchUserData.rejected, (state, action) => {
        state.isUserDataLoading = false;
        state.error = action.payload as string;
      });
  },
});

export const { logout } = authSlice.actions;
export default authSlice.reducer;
