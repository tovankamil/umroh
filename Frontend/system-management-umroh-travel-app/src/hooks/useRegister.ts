// src/hooks/useRegister.ts
import { useState, useCallback } from "react";
import { inputRegister } from "@/features/register/registerSlice";
import { useAppDispatch, useAppSelector } from "@/app/hooks";
import type { RegisterData } from "@/features/register/registerSlice";

export interface FormData {
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

export const useRegister = () => {
  const dispatch = useAppDispatch();
  const { loading, error, success, detailError } = useAppSelector(
    (state) => state.register
  );
  const [formData, setFormData] = useState<FormData>({
    username: "",
    name: "",
    email: "",
    password: "",
    first_name: "",
    last_name: "",
    phone_number: "",
    ktp: "",
    address: "",
    province: "",
    city: "",
    district: "",
    ahliwaris: "",
    postal_code: "",
    sponsor_username: "",
  });

  const handleRegisterWithFormData = useCallback(
    (formData: FormData) => {
      if (formData.username.trim()) {
        const registerData: RegisterData = {
          username: formData.username.trim(),
          name: formData.name,
          email: formData.email,
          password: formData.password,
          first_name: formData.first_name,
          last_name: formData.last_name,
          phone_number: formData.phone_number,
          ktp: formData.ktp,
          address: formData.address,
          province: formData.province,
          city: formData.city,
          district: formData.district,
          ahliwaris: formData.ahliwaris,
          postal_code: formData.postal_code,
          sponsor_username: formData.sponsor_username,
        };

        dispatch(inputRegister(registerData));
      }
    },
    [dispatch]
  );

  const handleRegisterWithUsername = useCallback(
    (username: string) => {
      if (username.trim()) {
        const registerData: RegisterData = {
          username: username.trim(),
          name: "",
          email: "",
          password: "",
          first_name: "",
          last_name: "",
          phone_number: "",
          ktp: "",
          address: "",
          province: "",
          city: "",
          district: "",
          ahliwaris: "",
          postal_code: "",
          sponsor_username: "",
        };

        dispatch(inputRegister(registerData));
      }
    },
    [dispatch]
  );

  return {
    handleRegisterWithFormData,
    handleRegisterWithUsername,
    loading,
    error,
    success,
    formData,
    detailError,
    setFormData,
  };
};
