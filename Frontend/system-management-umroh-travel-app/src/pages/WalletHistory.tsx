// @ts-nocheck
import React, { useState, useEffect, useMemo } from "react";
import { DashboardLayout } from "@/components/DashboardLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  ArrowLeft,
  ArrowRight,
  TrendingUp,
  TrendingDown,
  DollarSign,
  Loader2,
} from "lucide-react";

// --- DUMMY DATA ---
interface Transaction {
  id: string;
  date: string;
  description: string;
  amount: number;
  type: "DEBIT" | "KREDIT";
  balance: number;
}

const generateDummyTransactions = (count: number): Transaction[] => {
  const data: Transaction[] = [];
  let currentBalance = 5000000;

  for (let i = 0; i < count; i++) {
    const isCredit = Math.random() > 0.4; // Lebih banyak kredit
    const amount =
      Math.floor(Math.random() * (isCredit ? 1000000 : 500000)) + 100000;

    if (isCredit) {
      currentBalance += amount;
    } else {
      currentBalance -= amount;
    }

    const type = isCredit ? "KREDIT" : "DEBIT";
    const description = isCredit
      ? `Komisi Penjualan #${i + 1}`
      : `Pembelian Paket #${i + 1}`;

    data.push({
      id: `TXN-${1000 + i}`,
      date: new Date(Date.now() - i * 86400000).toLocaleDateString("id-ID"), // Mundur 1 hari
      description,
      amount,
      type,
      balance: currentBalance,
    });
  }
  return data.reverse(); // Urutkan dari yang terbaru
};

const DUMMY_TRANSACTIONS: Transaction[] = generateDummyTransactions(50); // 50 transaksi dummy

const formatCurrency = (value: number) => {
  return new Intl.NumberFormat("id-ID", {
    style: "currency",
    currency: "IDR",
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value);
};

// --- KOMPONEN UTAMA ---

const WalletHistory: React.FC = () => {
  const [currentPage, setCurrentPage] = useState(1);
  const [transactionsPerPage] = useState(10);
  const [isLoading, setIsLoading] = useState(true); // State untuk loading

  // Simulasikan waktu loading
  useEffect(() => {
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 1000);
    return () => clearTimeout(timer);
  }, []);

  // Logika Paging
  const indexOfLastTransaction = currentPage * transactionsPerPage;
  const indexOfFirstTransaction = indexOfLastTransaction - transactionsPerPage;

  const currentTransactions = useMemo(() => {
    return DUMMY_TRANSACTIONS.slice(
      indexOfFirstTransaction,
      indexOfLastTransaction
    );
  }, [currentPage, transactionsPerPage]);

  const totalPages = Math.ceil(DUMMY_TRANSACTIONS.length / transactionsPerPage);

  const paginate = (pageNumber: number) => {
    if (pageNumber >= 1 && pageNumber <= totalPages) {
      setCurrentPage(pageNumber);
    }
  };

  const currentBalance =
    DUMMY_TRANSACTIONS.length > 0 ? DUMMY_TRANSACTIONS[0].balance : 0;
  const totalCredit = DUMMY_TRANSACTIONS.filter(
    (t) => t.type === "KREDIT"
  ).reduce((sum, t) => sum + t.amount, 0);
  const totalDebit = DUMMY_TRANSACTIONS.filter(
    (t) => t.type === "DEBIT"
  ).reduce((sum, t) => sum + t.amount, 0);

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <h1 className="text-3xl font-bold text-gray-800">
          Riwayat Transaksi Dompet
        </h1>

        {/* Ringkasan Saldo dan Total */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card className="shadow-xl border-l-4 border-primary">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-gray-500">
                Saldo Saat Ini
              </CardTitle>
              <DollarSign className="h-4 w-4 text-primary" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-primary">
                {formatCurrency(currentBalance)}
              </div>
              <p className="text-xs text-gray-500 mt-1">
                Estimasi saldo real-time
              </p>
            </CardContent>
          </Card>

          <Card className="shadow-xl border-l-4 border-green-600">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-gray-500">
                Total Kredit (Masuk)
              </CardTitle>
              <TrendingUp className="h-4 w-4 text-green-600" />
            </CardHeader>
            <CardContent>
              <div className="text-xl font-bold text-green-700">
                {formatCurrency(totalCredit)}
              </div>
            </CardContent>
          </Card>

          <Card className="shadow-xl border-l-4 border-red-600">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-gray-500">
                Total Debit (Keluar)
              </CardTitle>
              <TrendingDown className="h-4 w-4 text-red-600" />
            </CardHeader>
            <CardContent>
              <div className="text-xl font-bold text-red-700">
                {formatCurrency(totalDebit)}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Tabel Riwayat Transaksi */}
        <Card className="shadow-2xl">
          <CardHeader>
            <CardTitle className="text-xl">
              Riwayat 50 Transaksi Terbaru
            </CardTitle>
          </CardHeader>

          <CardContent className="space-y-4">
            {isLoading ? (
              <div className="flex justify-center items-center h-64">
                <Loader2 className="h-10 w-10 animate-spin text-primary" />
                <span className="ml-3 text-lg text-gray-600">
                  Memuat transaksi...
                </span>
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      {[
                        "ID",
                        "Tanggal",
                        "Deskripsi",
                        "Tipe",
                        "Jumlah",
                        "Saldo Akhir",
                      ].map((header) => (
                        <th
                          key={header}
                          className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                        >
                          {header}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {currentTransactions.map((tx) => (
                      <tr
                        key={tx.id}
                        className="hover:bg-gray-50 transition-colors duration-150"
                      >
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                          {tx.id}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {tx.date}
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-900 max-w-xs truncate">
                          {tx.description}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span
                            className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                              tx.type === "KREDIT"
                                ? "bg-green-100 text-green-800"
                                : "bg-red-100 text-red-800"
                            }`}
                          >
                            {tx.type}
                          </span>
                        </td>
                        <td
                          className={`px-6 py-4 whitespace-nowrap text-sm font-semibold ${
                            tx.type === "KREDIT"
                              ? "text-green-600"
                              : "text-red-600"
                          }`}
                        >
                          {tx.type === "KREDIT" ? "+" : "-"}{" "}
                          {formatCurrency(tx.amount)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                          {formatCurrency(tx.balance)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}

            {/* Kontrol Paging */}
            <div className="flex justify-between items-center pt-4">
              <div className="text-sm text-gray-600">
                Menampilkan {indexOfFirstTransaction + 1} sampai{" "}
                {Math.min(indexOfLastTransaction, DUMMY_TRANSACTIONS.length)}{" "}
                dari {DUMMY_TRANSACTIONS.length} transaksi
              </div>
              <div className="flex space-x-2">
                {/* Tombol Sebelumnya */}
                <button
                  onClick={() => paginate(currentPage - 1)}
                  disabled={currentPage === 1 || isLoading}
                  className={`flex items-center px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
                    currentPage === 1
                      ? "bg-gray-200 text-gray-400 cursor-not-allowed"
                      : "bg-primary text-primary-foreground hover:bg-primary/90"
                  }`}
                >
                  <ArrowLeft className="h-4 w-4 mr-1" />
                  Sebelumnya
                </button>

                {/* Tombol Selanjutnya */}
                <button
                  onClick={() => paginate(currentPage + 1)}
                  disabled={currentPage === totalPages || isLoading}
                  className={`flex items-center px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
                    currentPage === totalPages
                      ? "bg-gray-200 text-gray-400 cursor-not-allowed"
                      : "bg-primary text-primary-foreground hover:bg-primary/90"
                  }`}
                >
                  Selanjutnya
                  <ArrowRight className="h-4 w-4 ml-1" />
                </button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
};

export default WalletHistory;
