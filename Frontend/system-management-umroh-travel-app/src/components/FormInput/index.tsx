// @ts-nocheck
import React, { memo } from "react";

/**
 * Helper component for form input fields.
 * It is memoized for performance optimization, ensuring it only re-renders
 * when its specific props change.
 */
const FormInput = memo(
  ({
    label,
    name,
    type = "text",
    icon,
    error,
    required = true,
    formData,
    handleChange,
    isSubmitting,
    addon, // New prop for the addon (e.g., check button)
  }) => (
    <div className="space-y-1">
      <label
        htmlFor={name}
        className="text-sm font-medium text-gray-700 flex items-center"
      >
        {icon}
        <span className="ml-2">
          {label} {required && <span className="text-red-500">*</span>}
        </span>
      </label>
      {/* Input and Addon Container */}
      <div className="flex items-start space-x-2">
        <input
          id={name}
          name={name}
          type={type}
          value={formData[name]}
          onChange={handleChange}
          required={required}
          // Using type='text' for number fields to enforce custom validation and prevent browser default behavior
          className={`w-full p-2 border rounded-lg focus:ring-primary focus:border-primary transition duration-150 ${
            error ? "border-red-500 focus:ring-red-500" : "border-gray-300"
          }`}
          disabled={isSubmitting}
        />
        {/* Render the addon if provided */}
        {addon && <div>{addon}</div>}
      </div>
      {error && <p className="text-xs text-red-500 mt-1">{error}</p>}
    </div>
  )
);

export default FormInput;
