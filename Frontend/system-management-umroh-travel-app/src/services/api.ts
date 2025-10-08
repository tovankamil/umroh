// src/services/api.ts
import axios from "axios";

// Buat instance axios dengan konfigurasi dasar
const api = axios.create({
  baseURL: import.meta.env.VITE_BACKEND_API_URL,
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: true,
});

// Request interceptor untuk menambahkan token ke header
api.interceptors.request.use(
  (config) => {
    // Ambil token dari localStorage
    const token = localStorage.getItem("token");

    // Jika token ada, tambahkan ke header Authorization
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    } else {
    }

    return config;
  },
  (error) => {
    // Handle request error
    console.error("Request error:", error);
    return Promise.reject(error);
  }
);

// Response interceptor untuk menangani error
api.interceptors.response.use(
  (response) => {
    // Logging untuk debugging

    return response;
  },
  (error) => {
    // Logging untuk debugging
    console.error("Response error:", error);

    // Jika response error (misalnya token expired)
    if (error.response && error.response.status === 401) {
      localStorage.removeItem("token");
      localStorage.removeItem("username"); // Tambahkan ini
      // Redirect ke halaman login
      window.location.href = "/login";
    }

    return Promise.reject(error);
  }
);

export default api;
