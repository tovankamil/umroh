// components/BankSelectionForm.tsx
import React, { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Search, Check, Building, Banknote } from "lucide-react";

interface Bank {
  name: string;
  bank_code: string;
}

interface BankSelectionFormProps {
  onBankSelect: (bank: Bank) => void;
  selectedBank?: Bank | null;
  disabled?: boolean;
}

const BankSelectionForm: React.FC<BankSelectionFormProps> = ({
  onBankSelect,
  selectedBank,
  disabled = false,
}) => {
  const [banks, setBanks] = useState<Bank[]>([]);
  const [filteredBanks, setFilteredBanks] = useState<Bank[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Simulasi fetch data bank dari API
  useEffect(() => {
    const fetchBanks = async () => {
      try {
        setLoading(true);
        // Ganti dengan API call sebenarnya
        // const response = await fetch('/api/banks');
        // const data = await response.json();

        // Data dummy berdasarkan response Anda
        const bankData: Bank[] = [
          { name: "Mandiri", bank_code: "mandiri" },
          { name: "BRI", bank_code: "bri" },
          { name: "BNI", bank_code: "bni" },
          { name: "BCA", bank_code: "bca" },
          { name: "BSI (Bank Syariah Indonesia)", bank_code: "bsm" },
          { name: "CIMB Niaga/CIMB Niaga Syariah", bank_code: "cimb" },
          { name: "Muamalat", bank_code: "muamalat" },
          { name: "Danamon / Danamon Syariah", bank_code: "danamon" },
          { name: "Bank Permata", bank_code: "permata" },
          { name: "Maybank Indonesia", bank_code: "bii" },
          { name: "Panin Bank", bank_code: "panin" },
          { name: "TMRW/UOB", bank_code: "uob" },
          { name: "OCBC NISP", bank_code: "ocbc" },
          { name: "Citibank", bank_code: "citibank" },
          { name: "Bank Artha Graha Internasional", bank_code: "artha" },
          { name: "Bank of Tokyo Mitsubishi UFJ", bank_code: "tokyo" },
          { name: "DBS Indonesia", bank_code: "dbs" },
          { name: "Standard Chartered Bank", bank_code: "standard_chartered" },
          { name: "Bank Capital Indonesia", bank_code: "capital" },
          { name: "ANZ Indonesia", bank_code: "anz" },
          { name: "Bank of China (Hong Kong) Limited", bank_code: "boc" },
          { name: "Bank Bumi Arta", bank_code: "bumi_arta" },
          { name: "HSBC Indonesia", bank_code: "hsbc" },
          { name: "Rabobank International Indonesia", bank_code: "rabobank" },
          { name: "Bank Mayapada", bank_code: "mayapada" },
          { name: "BJB", bank_code: "bjb" },
          { name: "Bank DKI Jakarta", bank_code: "dki" },
          { name: "BPD DIY", bank_code: "daerah_istimewa" },
          { name: "Bank Jateng", bank_code: "jawa_tengah" },
          { name: "Bank Jatim", bank_code: "jawa_timur" },
          { name: "Bank Contoh2", bank_code: "BANK0012" },
        ];

        setBanks(bankData);
        setFilteredBanks(bankData);
        setError(null);
      } catch (err) {
        setError("Gagal memuat data bank");
        console.error("Error fetching banks:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchBanks();
  }, []);

  // Filter banks berdasarkan search term
  useEffect(() => {
    if (searchTerm.trim() === "") {
      setFilteredBanks(banks);
    } else {
      const filtered = banks.filter(
        (bank) =>
          bank.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
          bank.bank_code.toLowerCase().includes(searchTerm.toLowerCase())
      );
      setFilteredBanks(filtered);
    }
  }, [searchTerm, banks]);

  const handleBankSelect = (bank: Bank) => {
    if (!disabled) {
      onBankSelect(bank);
    }
  };

  if (loading) {
    return (
      <Card className="shadow-2xl">
        <CardHeader>
          <CardTitle className="text-xl flex items-center text-primary">
            <Banknote className="h-5 w-5 mr-2" /> Pilih Bank
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex justify-center items-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
            <span className="ml-2 text-gray-600">Memuat data bank...</span>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className="shadow-2xl">
        <CardHeader>
          <CardTitle className="text-xl flex items-center text-primary">
            <Banknote className="h-5 w-5 mr-2" /> Pilih Bank
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8 text-red-600">
            <p>{error}</p>
            <button
              onClick={() => window.location.reload()}
              className="mt-4 px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary-dark"
            >
              Coba Lagi
            </button>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="shadow-2xl">
      <CardHeader>
        <CardTitle className="text-xl flex items-center text-primary">
          <Banknote className="h-5 w-5 mr-2" /> Pilih Bank
        </CardTitle>
        <p className="text-sm text-gray-600 mt-2">
          Pilih bank untuk rekening nasabah{" "}
          {selectedBank && `- Terpilih: ${selectedBank.name}`}
        </p>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Search Input */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
          <input
            type="text"
            placeholder="Cari bank berdasarkan nama atau kode..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
            disabled={disabled}
          />
        </div>

        {/* Bank List */}
        <div className="max-h-80 overflow-y-auto border border-gray-200 rounded-lg">
          {filteredBanks.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <Building className="h-12 w-12 mx-auto mb-2 text-gray-300" />
              <p>Tidak ada bank yang ditemukan</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 p-2">
              {filteredBanks.map((bank) => (
                <button
                  key={bank.bank_code}
                  type="button"
                  onClick={() => handleBankSelect(bank)}
                  disabled={disabled}
                  className={`
                    relative p-4 text-left border rounded-lg transition-all duration-200
                    ${
                      selectedBank?.bank_code === bank.bank_code
                        ? "border-primary bg-blue-50 ring-2 ring-primary ring-opacity-50"
                        : "border-gray-200 hover:border-primary hover:bg-gray-50"
                    }
                    ${
                      disabled
                        ? "opacity-50 cursor-not-allowed"
                        : "cursor-pointer"
                    }
                  `}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <p className="font-semibold text-gray-800 truncate">
                        {bank.name}
                      </p>
                      <p className="text-sm text-gray-500 mt-1">
                        Kode: {bank.bank_code}
                      </p>
                    </div>
                    {selectedBank?.bank_code === bank.bank_code && (
                      <Check className="h-5 w-5 text-primary flex-shrink-0 ml-2" />
                    )}
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Selected Bank Info */}
        {selectedBank && (
          <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
            <div className="flex items-center">
              <Check className="h-5 w-5 text-green-600 mr-2" />
              <div>
                <p className="font-semibold text-green-800">Bank Terpilih</p>
                <p className="text-green-700">{selectedBank.name}</p>
                <p className="text-sm text-green-600">
                  Kode: {selectedBank.bank_code}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Bank Count Info */}
        <div className="text-sm text-gray-500 text-center">
          Menampilkan {filteredBanks.length} dari {banks.length} bank
        </div>
      </CardContent>
    </Card>
  );
};

export default BankSelectionForm;
