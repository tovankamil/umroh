import api from "@/services/api";
import type { RegisterData } from "./registerSlice";

export const registerNewUser = async (
  data: RegisterData
): Promise<RegisterData> => {
  try {
    const response = await api.post(`/api/v1/registrasi/`, data);
    // Pastikan response structure sesuai dengan kebutuhan
    return response.data.data || response.data;
  } catch (error: any) {
    throw error;
  }
};
