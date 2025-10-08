// src/features/register/registerSlice.ts
import {
  createAsyncThunk,
  createSlice,
  type PayloadAction,
} from "@reduxjs/toolkit";
import { registerNewUser } from "./register";

// Interface untuk struktur error response
export interface ValidationError {
  message: string;
  errors: string[];
}

export interface RegisterData {
  username: string;
  name: string;
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  phone_number: string;
  ktp: string;
  address: string;
  province: string;
  city: string;
  district: string;
  ahliwaris: string;
  postal_code: string;
  sponsor_username: string;
}

export interface RegisterState {
  data: RegisterData | null;
  loading: boolean;
  error: string | null;
  detailError: string[] | null; // Diubah dari [] menjadi string[] | null
  success: boolean;
}

const initialState: RegisterState = {
  data: null,
  loading: false,
  error: null,
  detailError: null, // Diperbaiki inisialisasi
  success: false,
};

// Async thunk untuk registrasi user
export const inputRegister = createAsyncThunk(
  "register/inputRegister",
  async (data: RegisterData, { rejectWithValue }) => {
    try {
      const userData = await registerNewUser(data);
      return userData;
    } catch (error: any) {
      // Handle error response dengan struktur validasi
      if (error.response?.data) {
        return rejectWithValue(error.response.data);
      }
      return rejectWithValue({
        message: "Registration failed",
        errors: error.response.data.errors || [],
      });
    }
  }
);

const registerSlice = createSlice({
  name: "register",
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
      state.detailError = null;
    },
    resetRegister: (state) => {
      state.data = null;
      state.loading = false;
      state.error = null;
      state.detailError = null;
      state.success = false;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(inputRegister.pending, (state) => {
        state.loading = true;
        state.error = null;
        state.detailError = null;
        state.success = false;
      })
      .addCase(
        inputRegister.fulfilled,
        (state, action: PayloadAction<RegisterData>) => {
          state.loading = false;
          state.data = action.payload;
          state.success = true;
          state.error = null;
          state.detailError = null;
        }
      )
      .addCase(inputRegister.rejected, (state, action) => {
        state.loading = false;
        state.success = false;

        // Handle error dengan struktur validasi
        const errorPayload = action.payload as ValidationError;

        if (errorPayload && errorPayload.errors) {
          state.error = errorPayload.message || "Validasi gagal";
          state.detailError = errorPayload.errors;
        } else {
          state.error = (action.payload as string) || "Registration failed";
          state.detailError = null;
        }
      });
  },
});

export const { clearError, resetRegister } = registerSlice.actions;

// Selector yang sudah dikomentar (opsional untuk digunakan)
// export const selectRegister = (state: RootState) => state.register;
// export const selectRegisterLoading = (state: RootState) => state.register.loading;
// export const selectRegisterError = (state: RootState) => state.register.error;
// export const selectRegisterDetailError = (state: RootState) => state.register.detailError;
// export const selectRegisterSuccess = (state: RootState) => state.register.success;

export default registerSlice.reducer;
