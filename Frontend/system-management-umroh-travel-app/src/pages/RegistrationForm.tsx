// @ts-nocheck
import React, { useState, useEffect } from "react";
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
  Mail,
} from "lucide-react";
import FormInput from "@/components/FormInput";
import { useRegister } from "@/hooks/useRegister";
import ErrorModal from "@/components/ErrorModal";
import { validate } from "@/constants/validation";
import SuccessModal from "@/components/SuccessModal";

// Initial data structure for the form
const initialFormData = {
  username: "",
  password: "",
  sponsor_username: "",
  name: "",
  email: "",
  ktp: "",
  phone_number: "",
  address: "",
  province: "",
  city: "",
  district: "",
  postal_code: "",
  ahliwaris: "",
};

const RegistrationForm: React.FC = () => {
  const [formData, setFormData] = useState(initialFormData);
  const [errors, setErrors] = useState({});
  const [showErrorModal, setShowErrorModal] = useState(false);
  const [showSuccessModal, setShowSuccessModal] = useState(false);
  const [modalErrorMessage, setModalErrorMessage] = useState("");
  const [fieldErrors, setFieldErrors] = useState<string[]>([]);
  const [lastSubmittedData, setLastSubmittedData] = useState(null);

  const { handleRegisterWithFormData, loading, error, success, detailError } =
    useRegister();

  // Handle API error and success states
  useEffect(() => {
    console.log("detailError", detailError);
    if (error) {
      let cleanErrorMessage = "Terjadi kesalahan saat registrasi.";
      let extractedFieldErrors: string[] = [];

      if (typeof error === "string") {
        // If error is already a string
        cleanErrorMessage = error;
      } else if (error.response?.data) {
        const errorData = error.response.data;

        // Handle the specific format: {"message":"Validasi gagal.","errors":["username: Username sudah digunakan."]}
        if (errorData.message) {
          cleanErrorMessage = errorData.message;
        }

        if (errorData.errors && Array.isArray(errorData.errors)) {
          // Extract field errors from array format
          extractedFieldErrors = errorData.errors.map((errorItem) => {
            if (typeof errorItem === "string") {
              return errorItem;
            }
            return String(errorItem);
          });

          // Also update form field errors for inline display
          const newFieldErrors = {};
          errorData.errors.forEach((errorItem) => {
            if (typeof errorItem === "string") {
              // Extract field name from error message (format: "field_name: Error message")
              const fieldMatch = errorItem.match(/^(\w+):\s*(.+)/);
              if (fieldMatch) {
                const fieldName = fieldMatch[1];
                const errorMessage = fieldMatch[2];
                newFieldErrors[fieldName] = errorMessage;
              }
            }
          });
          setErrors((prev) => ({ ...prev, ...newFieldErrors }));
        }

        // Fallback for other error formats
        else if (errorData.detail) {
          cleanErrorMessage = errorData.detail;
        } else if (typeof errorData === "string") {
          cleanErrorMessage = errorData;
        }
      } else if (error.message) {
        cleanErrorMessage = error.message;
      }

      console.log("Processed error message:", cleanErrorMessage);
      console.log("Processed field errors:", extractedFieldErrors);

      setModalErrorMessage(cleanErrorMessage);
      setFieldErrors(detailError || extractedFieldErrors);
      setShowErrorModal(true);
    }
  }, [error]);

  useEffect(() => {
    if (success) {
      setShowSuccessModal(true);
      setFormData(initialFormData); // Reset form on success
      setLastSubmittedData(null);
      setErrors({});
      setFieldErrors([]);
    }
  }, [success]);

  // Handle input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    let newValue = value;

    // Filter non-digit characters for number-only fields
    if (["ktp", "phone_number", "postal_code"].includes(name)) {
      newValue = value.replace(/\D/g, "");
    }

    setFormData((prev) => ({ ...prev, [name]: newValue }));

    // Clear error when the user starts typing
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: undefined }));
    }
  };

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();

    // Clear previous errors
    setErrors({});
    setFieldErrors([]);

    // Validate form
    const formErrors = validate(formData);
    console.log("Form validation errors:", formErrors);

    if (Object.keys(formErrors).length > 0) {
      setErrors(formErrors);

      // Convert form errors to fieldErrors format for modal
      const errorList = Object.entries(formErrors).map(([field, message]) => {
        // Convert field name to more readable format
        const fieldName = field.replace(/_/g, " ");
        return `${fieldName}: ${message}`;
      });

      setModalErrorMessage("Validasi form gagal");
      setFieldErrors(errorList);
      setShowErrorModal(true);
      return;
    }

    setLastSubmittedData({ ...formData }); // Save data for retry
    handleRegisterWithFormData(formData);
  };

  // Retry submission with same data
  const handleRetry = () => {
    setShowErrorModal(false);
    if (lastSubmittedData) {
      // Auto-focus on username field if it's a username error
      if (
        modalErrorMessage.includes("username") ||
        fieldErrors.some((error) => error.toLowerCase().includes("username"))
      ) {
        const usernameInput = document.querySelector('input[name="username"]');
        if (usernameInput) {
          usernameInput.focus();
          usernameInput.select();
        }
      }

      // You can also resubmit automatically if needed
      // handleRegisterWithFormData(lastSubmittedData);
    }
  };

  // Close modals
  const closeErrorModal = () => {
    setShowErrorModal(false);
    setModalErrorMessage("");
    setFieldErrors([]);
  };

  const closeSuccessModal = () => {
    setShowSuccessModal(false);
  };

  // Define props that are consistently passed to FormInput
  const inputProps = {
    formData,
    handleChange,
    isSubmitting: loading,
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
          {/* Data Akun & Sponsor Card */}
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
              <FormInput
                label="Password"
                name="password"
                type="password"
                icon={<Key className="h-4 w-4" />}
                error={errors.password}
                {...inputProps}
              />
              <FormInput
                label="Email"
                name="email"
                type="email"
                icon={<Mail className="h-4 w-4" />}
                error={errors.email}
                {...inputProps}
              />
              <FormInput
                label="ID Sponsor"
                name="sponsor_username"
                icon={<UserPlus className="h-4 w-4" />}
                error={errors.sponsor_username}
                {...inputProps}
              />
            </CardContent>
          </Card>

          {/* Informasi Pribadi Card */}
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
                maxLength={16}
                icon={<Key className="h-4 w-4" />}
                error={errors.ktp}
                {...inputProps}
              />
              <FormInput
                label="Nomor Telepon (WhatsApp)"
                name="phone_number"
                type="text"
                icon={<Phone className="h-4 w-4" />}
                error={errors.phone_number}
                {...inputProps}
              />
              <FormInput
                label="Nama Ahli Waris"
                name="ahliwaris"
                icon={<User className="h-4 w-4" />}
                error={errors.ahliwaris}
                {...inputProps}
              />
            </CardContent>
          </Card>

          {/* Alamat Lengkap Card */}
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
                  name="postal_code"
                  type="text"
                  icon={<MapPin className="h-4 w-4" />}
                  error={errors.postal_code}
                  {...inputProps}
                />
              </div>
            </CardContent>
          </Card>

          {/* Submit Button */}
          <div className="flex justify-end pt-4">
            <button
              type="submit"
              disabled={loading}
              className="flex cursor-pointer items-center space-x-2 px-6 py-3 text-lg font-bold rounded-xl text-white bg-green-600 hover:bg-green-700 disabled:bg-gray-400 transition-colors shadow-lg transform hover:scale-[1.02] active:scale-100 disabled:transform-none"
            >
              {loading ? (
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

      {/* Error Modal */}
      <ErrorModal
        isOpen={showErrorModal}
        onClose={closeErrorModal}
        errorMessage={modalErrorMessage}
        fieldErrors={fieldErrors}
        onRetry={handleRetry}
      />

      {/* Success Modal */}
      <SuccessModal isOpen={showSuccessModal} onClose={closeSuccessModal} />
    </DashboardLayout>
  );
};

export default RegistrationForm;
