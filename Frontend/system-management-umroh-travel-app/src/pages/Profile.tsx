// src/pages/Dashboard.tsx
import Nav from "@/components/Nav";
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { DashboardLayout } from "@/components/DashboardLayout";

const Profile: React.FC = () => {
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

  // if (!userData) {
  //   return <Spinner />;
  // }

  return (
    <DashboardLayout>
      <div className="min-h-screen bg-gray-50">
        {/* Dashboard Content */}
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <div className="px-4 py-6 sm:px-0">
            {error && (
              <div className="mb-4 bg-red-50 text-red-700 p-3 rounded-md">
                Error: {error}
              </div>
            )}

            {isUserDataLoading ? (
              <div className="flex justify-center items-center h-64">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
              </div>
            ) : userData ? (
              <div className="bg-white shadow rounded-lg p-6">
                <h2 className="text-lg font-medium text-gray-900 mb-4">
                  User Information
                </h2>

                <div className="grid grid-cols-1 gap-x-4 gap-y-4 sm:grid-cols-2 mb-6">
                  <div className="sm:col-span-1">
                    <dt className="text-sm font-medium text-gray-500">
                      Username
                    </dt>
                    <dd className="mt-1 text-sm text-gray-900">
                      {userData.user.username}
                    </dd>
                  </div>
                  <div className="sm:col-span-1">
                    <dt className="text-sm font-medium text-gray-500">Name</dt>
                    <dd className="mt-1 text-sm text-gray-900">
                      {userData.user.name || "Not provided"}
                    </dd>
                  </div>
                  <div className="sm:col-span-1">
                    <dt className="text-sm font-medium text-gray-500">
                      Phone Number
                    </dt>
                    <dd className="mt-1 text-sm text-gray-900">
                      {/* {userData.user.phone_number} */}
                    </dd>
                  </div>
                  <div className="sm:col-span-1">
                    <dt className="text-sm font-medium text-gray-500">KTP</dt>
                    <dd className="mt-1 text-sm text-gray-900">
                      {userData.user.ktp}
                    </dd>
                  </div>
                  <div className="sm:col-span-1">
                    <dt className="text-sm font-medium text-gray-500">
                      Address
                    </dt>
                    <dd className="mt-1 text-sm text-gray-900">
                      {userData.user.address}
                    </dd>
                  </div>
                  <div className="sm:col-span-1">
                    <dt className="text-sm font-medium text-gray-500">
                      Province
                    </dt>
                    <dd className="mt-1 text-sm text-gray-900">
                      {userData.user.province}
                    </dd>
                  </div>
                  <div className="sm:col-span-1">
                    <dt className="text-sm font-medium text-gray-500">City</dt>
                    <dd className="mt-1 text-sm text-gray-900">
                      {userData.user.city}
                    </dd>
                  </div>
                  <div className="sm:col-span-1">
                    <dt className="text-sm font-medium text-gray-500">
                      District
                    </dt>
                    <dd className="mt-1 text-sm text-gray-900">
                      {userData.user.district}
                    </dd>
                  </div>
                  <div className="sm:col-span-1">
                    <dt className="text-sm font-medium text-gray-500">
                      Postal Code
                    </dt>
                    <dd className="mt-1 text-sm text-gray-900">
                      {userData.user.postal_code}
                    </dd>
                  </div>
                  <div className="sm:col-span-1">
                    <dt className="text-sm font-medium text-gray-500">
                      Level Status
                    </dt>
                    <dd className="mt-1 text-sm text-gray-900">
                      {userData.user.level_status}
                    </dd>
                  </div>
                </div>

                <div className="border-t border-gray-200 pt-4">
                  <h3 className="text-md font-medium text-gray-900 mb-2">
                    Sponsorships
                  </h3>
                  <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <h4 className="text-sm font-medium text-gray-500">
                        Sponsorships Received
                      </h4>
                      <p className="text-lg font-semibold">
                        {userData.sponsorships_received_count}
                      </p>
                    </div>
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <h4 className="text-sm font-medium text-gray-500">
                        Sponsorships Given
                      </h4>
                      <p className="text-lg font-semibold">
                        {userData.sponsorships_given_count}
                      </p>
                    </div>
                  </div>
                </div>

                <div className="mt-6 border-t border-gray-200 pt-4">
                  <h3 className="text-md font-medium text-gray-900 mb-2">
                    Dashboard Content
                  </h3>
                  <div className="border-2 border-dashed border-gray-300 rounded-lg h-64 flex items-center justify-center">
                    <p className="text-gray-500">
                      Your dashboard content will appear here
                    </p>
                  </div>
                </div>
              </div>
            ) : (
              <div className="bg-white shadow rounded-lg p-6">
                <div className="text-center">
                  <p className="text-gray-500">Failed to load user data</p>
                  <button
                    onClick={handleFetchUserData}
                    className="mt-4 px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
                  >
                    Retry
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default Profile;
