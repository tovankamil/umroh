// @ts-nocheck
/**
 * Validation function for the registration form data.
 * @param {object} formData - The current state of the form data.
 * @returns {object} An object containing validation errors, keyed by field name.
 */
export const validate = (formData) => {
  const newErrors = {};
  const { username, password, ktp, phoneNumber, postalCode } = formData;
  const numberRegex = /^\d+$/; // Regex for numbers only
  const usernameRegex = /^[a-zA-Z0-9]+$/; // Regex for alphanumeric only (no special chars)

  // Check all required fields first
  Object.keys(formData).forEach((key) => {
    if (!formData[key]) {
      // "This field is required."
      newErrors[key] = `Field ini wajib diisi.`;
    }
  });

  // --- Specific Validation Rules ---

  // 1. Username validation (min 3 characters, no special characters)
  if (username && username.length < 3) {
    // "Username must be at least 3 characters long."
    newErrors.username = "Username minimal 3 karakter.";
  } else if (username && !usernameRegex.test(username)) {
    // "Username must not contain special characters."
    newErrors.username = "Username tidak boleh mengandung karakter spesial.";
  }

  // 2. Password validation (min 6 characters)
  if (password && password.length < 6) {
    // "Password must be at least 6 characters long."
    newErrors.password = "Password minimal 6 karakter.";
  }

  // 3. KTP validation (numbers only)
  if (ktp && !numberRegex.test(ktp)) {
    // "KTP number must contain numbers only."
    newErrors.ktp = "Nomor KTP hanya boleh mengandung angka.";
  }

  if (ktp && ktp.length > 16) {
    newErrors.ktp = "KTP maksimal 16 karakter.";
  }

  // 4. Phone Number validation (numbers only)
  if (phoneNumber && !numberRegex.test(phoneNumber)) {
    // "Phone number must contain numbers only."
    newErrors.phoneNumber = "Nomor Telepon hanya boleh mengandung angka.";
  }

  // 5. Postal Code validation (numbers only)
  if (postalCode && !numberRegex.test(postalCode)) {
    // "Postal code must contain numbers only."
    newErrors.postalCode = "Kode Pos hanya boleh mengandung angka.";
  }

  if (!formData.email.trim()) {
    newErrors.email = "Email wajib diisi";
  } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
    newErrors.email = "Format email tidak valid";
  }
  return newErrors;
};
