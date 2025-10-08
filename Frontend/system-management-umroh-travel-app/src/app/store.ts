// src/app/store.ts
import { configureStore } from "@reduxjs/toolkit";
import authReducer from "../features/auth/authSlice";
import registerReducer from "@/features/register/registerSlice";

export const store = configureStore({
  reducer: {
    auth: authReducer,
    register: registerReducer, // Tambahkan reducer register
  },
});

// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
