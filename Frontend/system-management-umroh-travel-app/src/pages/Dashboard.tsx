// @ts-nocheck
// src/pages/Dashboard.tsx
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { DashboardLayout } from "@/components/DashboardLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
// Menghapus semua impor recharts yang menyebabkan error
// import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line, AreaChart, Area } from 'recharts';
import { User, DollarSign, TrendingUp, Users } from "lucide-react";

// --- DUMMY DATA ---

// Data untuk pertumbuhan mitra per bulan (6 bulan terakhir)
const mitraData = [
  { name: "Mei", newMitra: 150, totalMitra: 800, height: 40 },
  { name: "Jun", newMitra: 180, totalMitra: 980, height: 48 },
  { name: "Jul", newMitra: 220, totalMitra: 1200, height: 58 },
  { name: "Agu", newMitra: 100, totalMitra: 1300, height: 30 },
  { name: "Sep", newMitra: 350, totalMitra: 1650, height: 90 },
  { name: "Okt", newMitra: 200, totalMitra: 1850, height: 50 },
];

// Data untuk perkembangan pendapatan (6 bulan terakhir)
const pendapatanData = [
  { name: "Mei", Pendapatan: 15000000, point: "10,80" },
  { name: "Jun", Pendapatan: 18000000, point: "60,70" },
  { name: "Jul", Pendapatan: 25000000, point: "110,50" },
  { name: "Agu", Pendapatan: 12000000, point: "160,90" },
  { name: "Sep", Pendapatan: 30000000, point: "210,30" },
  { name: "Okt", Pendapatan: 22000000, point: "260,65" },
];

// Ringkasan Statistik
const totalMitra = 1850; // Total dari dummy data bulan terakhir
const totalRevenue = 20000000; // Sesuai permintaan

// --- KOMPONEN PLACEHOLDER GRAFIK ---

// Placeholder untuk Area Chart (Pertumbuhan Mitra)
const MitraAreaChartPlaceholder = () => (
  <div className="relative h-full w-full p-4 border rounded-lg bg-gray-50 flex flex-col justify-end overflow-hidden">
    <div className="absolute top-0 left-0 p-3 text-xs text-gray-500 font-medium">
      Mitra Baru: 350 (Sep)
    </div>
    <div className="flex justify-between items-end h-3/4 w-full">
      {mitraData.map((data, index) => (
        <div
          key={index}
          className="flex flex-col items-center h-full justify-end"
        >
          {/* Bar */}
          <div
            className="w-4 bg-primary/80 rounded-t-sm transition-all duration-500 hover:bg-primary"
            style={{ height: `${data.height}%` }}
            title={`${data.name}: ${data.newMitra}`}
          ></div>
          {/* Label X-Axis */}
          <span className="text-xs text-gray-600 mt-1">{data.name}</span>
        </div>
      ))}
    </div>
    <div className="absolute bottom-0 left-0 w-full h-1 bg-gray-300"></div>
  </div>
);

// Placeholder untuk Line Chart (Perkembangan Pendapatan)
const PendapatanLineChartPlaceholder = () => {
  // Membuat string titik untuk polyline SVG
  const pointsString = pendapatanData.map((d) => d.point).join(" ");

  return (
    <svg viewBox="0 0 300 100" className="w-full h-full">
      {/* Grid Y-Axis sederhana */}
      <line
        x1="10"
        y1="20"
        x2="290"
        y2="20"
        stroke="#e0e0e0"
        strokeDasharray="2"
      />
      <line
        x1="10"
        y1="50"
        x2="290"
        y2="50"
        stroke="#e0e0e0"
        strokeDasharray="2"
      />
      <line
        x1="10"
        y1="80"
        x2="290"
        y2="80"
        stroke="#e0e0e0"
        strokeDasharray="2"
      />

      {/* Garis Dasar X-Axis */}
      <line x1="10" y1="95" x2="290" y2="95" stroke="#333" />

      {/* Garis Data (Line Chart) */}
      <polyline
        fill="none"
        stroke="#FFC107"
        strokeWidth="3"
        points={pointsString}
      />

      {/* Titik Data dan Label X-Axis */}
      {pendapatanData.map((data, index) => (
        <React.Fragment key={index}>
          {/* Titik data */}
          <circle
            cx={data.point.split(",")[0]}
            cy={data.point.split(",")[1]}
            r="4"
            fill="#FFC107"
            stroke="white"
            strokeWidth="2"
          />
          {/* Label bulan (X-Axis) */}
          <text
            x={data.point.split(",")[0]}
            y="100"
            textAnchor="middle"
            fontSize="8"
            fill="#333"
          >
            {data.name}
          </text>
        </React.Fragment>
      ))}

      {/* Label Y-Axis Sederhana (Contoh) */}
      <text x="5" y="20" textAnchor="end" fontSize="8" fill="#333">
        30M
      </text>
      <text x="5" y="95" textAnchor="end" fontSize="8" fill="#333">
        10M
      </text>
    </svg>
  );
};

// --- KOMPONEN UTAMA DASHBOARD ---

const Dashboard: React.FC = () => {
  const {
    handleLogout,
    isAuthenticated,
    userData,
    isUserDataLoading,
    handleFetchUserData,
    error,
  } = useAuth();
  const navigate = useNavigate();
  const [isLoggingOut, setIsLoggingOut] = useState(false);

  // Ambil data user saat komponen dimuat
  useEffect(() => {
    if (isAuthenticated && !userData) {
      handleFetchUserData();
    }
  }, []);

  const handleLogoutClick = async () => {
    setIsLoggingOut(true);
    try {
      await new Promise((resolve) => setTimeout(resolve, 500));
      handleLogout();
      navigate("/login");
    } catch (error) {
      console.error("Logout failed:", error);
    } finally {
      setIsLoggingOut(false);
    }
  };

  // Fungsi untuk format mata uang IDR
  const formatCurrency = (value) => {
    return new Intl.NumberFormat("id-ID", {
      style: "currency",
      currency: "IDR",
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  return (
    // DashboardLayout akan menyediakan Header dan Sidebar
    <DashboardLayout>
      <div className="w-full space-y-8">
        <h1 className="text-3xl font-bold text-gray-800">Dashboard Utama</h1>

        {/* --- 1. RINGKASAN STATISTIK --- */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {/* Kartu: Total Mitra Bergabung */}
          <Card className="shadow-lg hover:shadow-xl transition-shadow border-l-4 border-primary">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-gray-500">
                Total Mitra Tergabung
              </CardTitle>
              <Users className="h-4 w-4 text-primary" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {totalMitra.toLocaleString("id-ID")}
              </div>
              <p className="text-xs text-gray-500 mt-1">+15% dari bulan lalu</p>
            </CardContent>
          </Card>

          {/* Kartu: Pendapatan Bulan Ini (Total) */}
          <Card className="shadow-lg hover:shadow-xl transition-shadow border-l-4 border-yellow-600">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-gray-500">
                Pendapatan Bulan Ini
              </CardTitle>
              <DollarSign className="h-4 w-4 text-yellow-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-yellow-700">
                {formatCurrency(totalRevenue)}
              </div>
              <p className="text-xs text-gray-500 mt-1">
                Target bulan ini tercapai
              </p>
            </CardContent>
          </Card>

          {/* Kartu: Mitra Baru Bulan Ini */}
          <Card className="shadow-lg hover:shadow-xl transition-shadow border-l-4 border-green-500">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-gray-500">
                Mitra Baru (Okt)
              </CardTitle>
              <User className="h-4 w-4 text-green-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {mitraData[mitraData.length - 1].newMitra.toLocaleString(
                  "id-ID"
                )}
              </div>
              <p className="text-xs text-gray-500 mt-1">
                Tertinggi dalam 3 bulan
              </p>
            </CardContent>
          </Card>

          {/* Kartu: Tren Kunjungan */}
          <Card className="shadow-lg hover:shadow-xl transition-shadow border-l-4 border-indigo-500">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-gray-500">
                Aktivitas Pendaftaran
              </CardTitle>
              <TrendingUp className="h-4 w-4 text-indigo-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">+5.30%</div>
              <p className="text-xs text-gray-500 mt-1">
                Dibandingkan minggu lalu
              </p>
            </CardContent>
          </Card>
        </div>

        {/* --- 2. GRAFIK PERKEMBANGAN --- */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Grafik 1: Pertumbuhan Mitra (Menggunakan Placeholder) */}
          <Card className="shadow-lg p-4">
            <CardHeader>
              <CardTitle className="text-lg font-semibold">
                Pertumbuhan Mitra Baru (6 Bulan)
              </CardTitle>
            </CardHeader>
            <CardContent className="h-80">
              <MitraAreaChartPlaceholder />
            </CardContent>
          </Card>

          {/* Grafik 2: Perkembangan Pendapatan (Menggunakan Placeholder) */}
          <Card className="shadow-lg p-4">
            <CardHeader>
              <CardTitle className="text-lg font-semibold">
                Perkembangan Pendapatan (6 Bulan)
              </CardTitle>
            </CardHeader>
            <CardContent className="h-80">
              <PendapatanLineChartPlaceholder />
            </CardContent>
          </Card>
        </div>

        {/* --- 3. DETAIL USER (Dari data yang sudah ada) --- */}
        {/* Konten detail user yang sebelumnya sudah ada (disembunyikan untuk tampilan bersih) */}
        {/* Hapus atau sisakan div ini sesuai kebutuhan */}
        {userData && (
          <div className="bg-white shadow rounded-lg p-6 mt-8">
            <h2 className="text-xl font-semibold mb-4 text-primary">
              Detail Profil Anda
            </h2>
            <p className="text-sm text-gray-600">
              Username:{" "}
              <span className="font-medium text-gray-800">
                {userData.user.username}
              </span>
            </p>
            <p className="text-sm text-gray-600">
              Level:{" "}
              <span className="font-medium text-primary">
                {userData.user.level_status}
              </span>
            </p>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
};

export default Dashboard;
