/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_BACKEND_API_URL: string;
  // Tambahkan env vars lainnya
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
