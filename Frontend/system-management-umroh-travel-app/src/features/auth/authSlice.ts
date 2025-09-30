import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { login, type AuthResponse, type LoginCredentials } from "./authService";
import type { PayloadAction } from "@reduxjs/toolkit";

// Definisikan tipe user yang lebih lengkap
interface User {
  id: string;
  username: string;
  name: string | null;
  email: string;
  level_status: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  error: string | null;
}

const initialState: AuthState = {
  user: null,
  token: localStorage.getItem("token"),
  isLoading: false,
  isAuthenticated: false,
  error: null,
};

export const loginUser = createAsyncThunk(
  "auth/loginUser",
  async (credentials: LoginCredentials, { rejectWithValue }) => {
    try {
      const response = await login(credentials);
      // Simpan access_token ke localStorage
      localStorage.setItem("token", response.data.access_token);

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

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    logout: (state) => {
      state.user = null;
      state.token = null;
      localStorage.removeItem("token");
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
        state.isAuthenticated = true;
        state.error = null;
        state.user = action.payload.user;
        state.token = action.payload.token;
      })
      .addCase(loginUser.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });
  },
});

export const { logout } = authSlice.actions;
export default authSlice.reducer;
