// @ts-nocheck
import React, { useState, memo } from "react";
import { DashboardLayout } from "@/components/DashboardLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  UserPlus,
  Save,
  Loader2,
  User,
  Home,
  Key,
  Phone,
  MapPin,
} from "lucide-react";
import FormInput from "@/components/FormInput";
import { validate } from "@/constants/validation";

// Initial data structure for the form, including the new 'password' field.
const initialFormData = {
  username: "",
  password: "", // New field for password
  sponsor: "",
  name: "",
  ktp: "",
  phoneNumber: "",
  address: "",
  province: "",
  city: "",
  district: "",
  postalCode: "",
  heir: "", // ahliwaris (heir)
};

// Helper component for input fields, defined outside and memoized for performance
// Props are passed explicitly from the parent component.

/**
 * Component for New Partner Registration Form.
 */
const RegistrationForm: React.FC = () => {
  const [formData, setFormData] = useState(initialFormData);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errors, setErrors] = useState({});

  // Handle input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    let newValue = value;

    // Filter non-digit characters for number-only fields (KTP, Phone, Postal Code)
    if (["ktp", "phoneNumber", "postalCode"].includes(name)) {
      newValue = value.replace(/\D/g, "");
    }

    setFormData((prev) => ({ ...prev, [name]: newValue }));

    // Clear error when the user starts typing
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: undefined }));
    }
  };

  // Comprehensive validation function implementing all rules

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    if (!validate()) {
      console.error("Validation failed.");
      return;
    }

    setIsSubmitting(true);

    // Simulate API registration call
    setTimeout(() => {
      console.log("Data registered:", formData);
      setFormData(initialFormData); // Reset form upon success
      setIsSubmitting(false);
      // Replaced alert() with console.log and a success message in the console
      console.log("Registrasi Mitra Baru Berhasil! (Data dicetak ke konsol)");
    }, 2000);
  };

  // Define props that are consistently passed to FormInput
  const inputProps = {
    formData,
    handleChange,
    isSubmitting,
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <h1 className="text-3xl font-bold text-gray-800 flex items-center">
          <UserPlus className="h-7 w-7 mr-3 text-primary" />
          Form Registrasi Mitra Baru
        </h1>
        <p className="text-gray-600">
          Mohon isi semua data wajib yang diperlukan untuk pendaftaran mitra
          baru.
        </p>

        <form onSubmit={handleSubmit} className="max-w-5xl mx-auto space-y-8">
          <Card className="shadow-2xl">
            <CardHeader>
              <CardTitle className="text-xl flex items-center text-primary">
                <Key className="h-5 w-5 mr-2" /> Data Akun & Sponsor
              </CardTitle>
            </CardHeader>
            <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <FormInput
                label="Username (ID Mitra)"
                name="username"
                icon={<User className="h-4 w-4" />}
                error={errors.username}
                {...inputProps}
              />
              <FormInput // Added Password Field
                label="Password"
                name="password"
                type="password"
                icon={<Key className="h-4 w-4" />}
                error={errors.password}
                {...inputProps}
              />
              <FormInput
                label="ID Sponsor"
                name="sponsor"
                icon={<UserPlus className="h-4 w-4" />}
                error={errors.sponsor}
                {...inputProps}
              />
              <div className="md:col-span-2">
                {/* Empty space for alignment */}
              </div>
            </CardContent>
          </Card>

          <Card className="shadow-2xl">
            <CardHeader>
              <CardTitle className="text-xl flex items-center text-primary">
                <User className="h-5 w-5 mr-2" /> Informasi Pribadi
              </CardTitle>
            </CardHeader>
            <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <FormInput
                label="Nama Lengkap"
                name="name"
                icon={<User className="h-4 w-4" />}
                error={errors.name}
                {...inputProps}
              />
              <FormInput
                label="Nomor KTP"
                name="ktp"
                type="text"
                icon={<Key className="h-4 w-4" />}
                error={errors.ktp}
                {...inputProps}
              />
              <FormInput
                label="Nomor Telepon (WhatsApp)"
                name="phoneNumber"
                type="text"
                icon={<Phone className="h-4 w-4" />}
                error={errors.phoneNumber}
                {...inputProps}
              />
              <FormInput
                label="Nama Ahli Waris"
                name="heir"
                icon={<User className="h-4 w-4" />}
                error={errors.heir}
                {...inputProps}
              />
            </CardContent>
          </Card>

          <Card className="shadow-2xl">
            <CardHeader>
              <CardTitle className="text-xl flex items-center text-primary">
                <Home className="h-5 w-5 mr-2" /> Alamat Lengkap
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <FormInput
                label="Alamat Detail (Jalan, Nomor Rumah, RT/RW)"
                name="address"
                icon={<MapPin className="h-4 w-4" />}
                error={errors.address}
                {...inputProps}
              />
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                <FormInput
                  label="Provinsi"
                  name="province"
                  icon={<MapPin className="h-4 w-4" />}
                  error={errors.province}
                  {...inputProps}
                />
                <FormInput
                  label="Kota/Kabupaten"
                  name="city"
                  icon={<MapPin className="h-4 w-4" />}
                  error={errors.city}
                  {...inputProps}
                />
                <FormInput
                  label="Kecamatan"
                  name="district"
                  icon={<MapPin className="h-4 w-4" />}
                  error={errors.district}
                  {...inputProps}
                />
                <FormInput
                  label="Kode Pos"
                  name="postalCode"
                  type="text"
                  icon={<MapPin className="h-4 w-4" />}
                  error={errors.postalCode}
                  {...inputProps}
                />
              </div>
            </CardContent>
          </Card>

          {/* Submit Button */}
          <div className="flex justify-end pt-4 ">
            <button
              type="submit"
              disabled={isSubmitting}
              className="flex cursor-pointer items-center space-x-2 px-6 py-3 text-lg font-bold rounded-xl text-white bg-green-600 hover:bg-green-700 disabled:bg-gray-400 transition-colors shadow-lg transform hover:scale-[1.02] active:scale-100"
            >
              {isSubmitting ? (
                <>
                  <Loader2 className="h-5 w-5 animate-spin" />
                  <span>Mendaftar...</span>
                </>
              ) : (
                <>
                  <Save className="h-5 w-5" />
                  <span>Daftarkan Mitra Baru</span>
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </DashboardLayout>
  );
};

export default RegistrationForm;
