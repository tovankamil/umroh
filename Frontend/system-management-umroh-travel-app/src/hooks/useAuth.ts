// src/hooks/useAuth.ts
import { useAppDispatch, useAppSelector } from "../app/hooks";
import {
  fetchUserData,
  logout,
  verifyTokenAuth,
} from "../features/auth/authSlice";

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
    if (username) {
      dispatch(fetchUserData(username));
    }
  };

  const verifyToken = async () => {
    const token = localStorage.getItem("token");
    if (!token) {
      return false;
    } else {
      dispatch(verifyTokenAuth(token));
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
    verifyToken,
  };
};
