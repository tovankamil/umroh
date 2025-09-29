import { useSelector, useDispatch } from "react-redux";

import { logout } from "../features/auth/authSlice";
import type { RootState } from "@/app/store";

export const useAuth = () => {
  const { user, token, isLoading, error } = useSelector(
    (state: RootState) => state.auth
  );
  const dispatch = useDispatch();

  const handleLogout = () => {
    dispatch(logout());
  };

  return {
    user,
    token,
    isLoading,
    error,
    handleLogout,
    isAuthenticated: !!token,
  };
};
