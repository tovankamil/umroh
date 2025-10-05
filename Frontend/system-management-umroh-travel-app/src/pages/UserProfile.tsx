// @ts-nocheck
import React, { useState, useEffect } from "react";
import { DashboardLayout } from "@/components/DashboardLayout"; // Menggunakan Layout yang ada
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  User,
  Mail,
  Phone,
  MapPin,
  Edit3,
  Save,
  Loader2,
  Calendar,
} from "lucide-react";

// --- DUMMY DATA ---
interface UserProfileData {
  name: string;
  email: string;
  phone: string;
  address: string;
  memberSince: string;
  lastLogin: string;
  level: string;
}

const DUMMY_USER_DATA: UserProfileData = {
  name: "Budi Santoso",
  email: "budi.santoso@mitra.com",
  phone: "+62 812 3456 7890",
  address: "Jl. Merdeka No. 10, Jakarta Pusat, DKI Jakarta",
  memberSince: "15 Januari 2022",
  lastLogin: "Baru saja",
  level: "Gold Partner",
};

/**
 * Komponen untuk menampilkan dan mengedit informasi Profil Pengguna.
 */
const UserProfile: React.FC = () => {
  const [userData, setUserData] = useState(DUMMY_USER_DATA);
  const [isEditing, setIsEditing] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [editedData, setEditedData] = useState(DUMMY_USER_DATA);

  // Handle perubahan input
  const handleChange = (e) => {
    const { name, value } = e.target;
    setEditedData((prev) => ({ ...prev, [name]: value }));
  };

  // Simulasikan proses penyimpanan data
  const handleSave = () => {
    setIsSaving(true);
    // Dalam aplikasi nyata: panggil API untuk menyimpan data
    setTimeout(() => {
      setUserData(editedData); // Update data utama
      setIsEditing(false);
      setIsSaving(false);
      console.log("Data profil berhasil disimpan.");
      // Di sini bisa ditambahkan notifikasi sukses
    }, 1500);
  };

  const handleEdit = () => {
    setEditedData(userData); // Set data yang akan diedit ke data saat ini
    setIsEditing(true);
  };

  // Komponen pembantu untuk menampilkan field
  const InfoField: React.FC<{
    icon: React.ReactNode;
    label: string;
    value: string;
    name: keyof UserProfileData;
    isEditable: boolean;
  }> = ({ icon, label, value, name, isEditable }) => (
    <div className="flex items-start space-x-4 py-3 border-b border-gray-100 last:border-b-0">
      <div className="text-primary pt-1 flex-shrink-0">{icon}</div>
      <div className="flex-1">
        <p className="text-xs font-medium uppercase text-gray-500">{label}</p>
        {isEditable && isEditing ? (
          <input
            type={name === "email" ? "email" : "text"}
            name={name}
            value={editedData[name]}
            onChange={handleChange}
            disabled={isSaving}
            className="w-full text-base font-semibold text-gray-800 bg-gray-50 border border-gray-200 rounded-lg p-1 mt-1 focus:ring-primary focus:border-primary transition duration-150"
          />
        ) : (
          <p className="text-base font-semibold text-gray-800 break-words">
            {value}
          </p>
        )}
      </div>
    </div>
  );

  return (
    // Gunakan DashboardLayout untuk menjaga konsistensi tampilan
    <DashboardLayout>
      <div className="space-y-6">
        <h1 className="text-3xl font-bold text-gray-800">Profil Saya</h1>
        <p className="text-gray-600">
          Kelola informasi pribadi dan detail kemitraan Anda.
        </p>

        <Card className="shadow-2xl max-w-4xl mx-auto">
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle className="text-2xl">Informasi Akun</CardTitle>

            {/* Tombol Edit/Simpan */}
            {!isEditing ? (
              <button
                onClick={handleEdit}
                className="flex items-center space-x-1 px-4 py-2 text-sm font-medium rounded-lg text-primary bg-primary/10 hover:bg-primary/20 transition-colors"
              >
                <Edit3 className="h-4 w-4" />
                <span>Edit Profil</span>
              </button>
            ) : (
              <button
                onClick={handleSave}
                disabled={isSaving}
                className="flex items-center space-x-1 px-4 py-2 text-sm font-medium rounded-lg text-white bg-green-600 hover:bg-green-700 disabled:bg-gray-400 transition-colors shadow-md"
              >
                {isSaving ? (
                  <Loader2 className="h-4 w-4 mr-1 animate-spin" />
                ) : (
                  <Save className="h-4 w-4" />
                )}
                <span>{isSaving ? "Menyimpan..." : "Simpan Perubahan"}</span>
              </button>
            )}
          </CardHeader>

          <CardContent className="space-y-4">
            {/* Bagian Foto Profil dan Level (Di atas form) */}
            <div className="flex items-center space-x-6 pb-6 border-b border-gray-200">
              <div className="relative w-20 h-20 rounded-full bg-gray-200 flex items-center justify-center border-4 border-primary shadow-lg">
                <User className="w-10 h-10 text-primary" />
              </div>
              <div>
                <h2 className="text-xl font-bold text-gray-900">
                  {userData.name}
                </h2>
                <span className="inline-flex items-center px-3 py-1 mt-1 rounded-full text-sm font-medium bg-yellow-500 text-white shadow-sm">
                  {userData.level}
                </span>
              </div>
            </div>

            {/* Grid Informasi Kontak dan Pribadi */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-10">
              {/* Kolom Kiri: Informasi Kontak */}
              <div className="space-y-2">
                <h3 className="text-lg font-semibold text-gray-700 mt-4 mb-2">
                  Detail Kontak
                </h3>
                <InfoField
                  icon={<User className="h-5 w-5" />}
                  label="Nama Lengkap"
                  value={userData.name}
                  name="name"
                  isEditable={true}
                />
                <InfoField
                  icon={<Mail className="h-5 w-5" />}
                  label="Email"
                  value={userData.email}
                  name="email"
                  isEditable={false} // Email biasanya tidak dapat diedit langsung
                />
                <InfoField
                  icon={<Phone className="h-5 w-5" />}
                  label="Nomor Telepon"
                  value={userData.phone}
                  name="phone"
                  isEditable={true}
                />
              </div>

              {/* Kolom Kanan: Informasi Lain */}
              <div className="space-y-2">
                <h3 className="text-lg font-semibold text-gray-700 mt-4 mb-2">
                  Detail Lainnya
                </h3>
                <InfoField
                  icon={<Calendar className="h-5 w-5" />}
                  label="Anggota Sejak"
                  value={userData.memberSince}
                  name="memberSince"
                  isEditable={false}
                />
                <InfoField
                  icon={<Calendar className="h-5 w-5" />}
                  label="Login Terakhir"
                  value={userData.lastLogin}
                  name="lastLogin"
                  isEditable={false}
                />
                <InfoField
                  icon={<MapPin className="h-5 w-5" />}
                  label="Alamat"
                  value={userData.address}
                  name="address"
                  isEditable={true}
                />
              </div>
            </div>

            {/* Tombol Simpan/Batal di bawah (hanya tampil saat mode edit) */}
            {isEditing && (
              <div className="flex justify-end space-x-4 pt-6 border-t border-gray-200">
                <button
                  onClick={() => setIsEditing(false)}
                  className="px-4 py-2 text-sm font-medium rounded-lg text-gray-700 border border-gray-300 hover:bg-gray-100 transition-colors"
                >
                  Batal
                </button>
                <button
                  onClick={handleSave}
                  disabled={isSaving}
                  className="px-4 py-2 text-sm font-medium rounded-lg text-white bg-primary hover:bg-primary/90 disabled:bg-gray-400 transition-colors"
                >
                  {isSaving ? "Menyimpan..." : "Simpan"}
                </button>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
};

export default UserProfile;
