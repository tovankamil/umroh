// src/hooks/useAuth.ts
import { useAppDispatch, useAppSelector } from "../app/hooks";
import { fetchUserData, logout } from "../features/auth/authSlice";

export const useAuth = () => {
  const {
    user,
    username,
    token,
    isLoading,
    error,
    userData,
    isUserDataLoading,
  } = useAppSelector((state) => state.auth);
  const dispatch = useAppDispatch();

  const handleLogout = () => {
    dispatch(logout());
  };

  const handleFetchUserData = () => {
    console.log(username);
    // Pastikan username ada sebelum mengambil data
    if (username) {
      dispatch(fetchUserData(username));
    }
  };

  // Hitung isAuthenticated dari token
  const isAuthenticated = !!token;

  return {
    user,
    username,
    token,
    isLoading,
    error,
    userData,
    isUserDataLoading,
    handleLogout,
    handleFetchUserData,
    isAuthenticated,
  };
};
