import { AlertCircle, X } from "lucide-react";
import { type FC } from "react";

interface ErrorModalProps {
  isOpen: boolean;
  onClose: () => void;
  errorMessage: string;
  onRetry: () => void;
  fieldErrors?: string[]; // Optional array of field-specific error messages
}

const ErrorModal: FC<ErrorModalProps> = ({
  isOpen,
  onClose,
  errorMessage,
  onRetry,
  fieldErrors,
}) => {
  if (!isOpen) return null;
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-auto">
        <div className="flex items-center justify-between p-6 border-b">
          <div className="flex items-center space-x-3">
            <div className="flex-shrink-0">
              <AlertCircle className="h-6 w-6 text-red-500" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900">
              Registration Error
            </h3>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        <div className="p-6">
          <div className="bg-red-50 border border-red-200 rounded-md p-4 mb-4">
            <p className="text-red-700 font-medium mb-2">{errorMessage}</p>

            {/* Display field-specific errors */}
            {fieldErrors && fieldErrors.length > 0 && (
              <div className="mt-3">
                <p className="text-red-600 text-sm font-medium mb-2">
                  Detail Error:
                </p>
                <ul className="list-disc list-inside space-y-1">
                  {fieldErrors.map((error, index) => (
                    <li key={index} className="text-red-600 text-sm">
                      {error}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          <p className="text-gray-600 text-sm mb-4">
            Silakan periksa data yang Anda masukkan dan coba lagi.
          </p>

          <div className="flex justify-end space-x-3">
            <button
              onClick={onClose}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md transition-colors"
            >
              Close
            </button>
            <button
              onClick={onRetry}
              className="px-4 py-2 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-md transition-colors"
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ErrorModal;
