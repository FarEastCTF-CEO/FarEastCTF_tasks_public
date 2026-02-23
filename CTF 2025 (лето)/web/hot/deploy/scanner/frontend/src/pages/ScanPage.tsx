// src/pages/ScanPage.tsx
import React, { useState } from "react";
import axios from "axios";
import Layout from "../components/Layout";
const apiUrl = import.meta.env.VITE_API_URL;


export default function ScanPage() {
  const [url, setUrl] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState("");

  const handleScanUrl = async () => {
    try {
      await axios.post(`${apiUrl}/api/scan/url`, { url });
      setMessage("Сканирование по URL запущено");
    } catch {
      setMessage("Ошибка при запуске сканирования");
    }
  };

  const handleScanSwagger = async () => {
    if (!file) return;
    const form = new FormData();
    form.append("swagger", file);
    try {
      await axios.post(`${apiUrl}/api/scan/swagger`, form, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setMessage("Сканирование swagger.yaml запущено");
    } catch {
      setMessage("Ошибка при загрузке swagger-файла");
    }
  };

  return (
    <Layout>
      <div className="space-y-6 max-w-xl mx-auto">
        <h1 className="text-2xl font-semibold">Запуск сканирования</h1>

        <div className="bg-white p-4 rounded shadow border">
          <label className="block font-medium mb-1">URL сайта:</label>
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://example.com"
            className="w-full border rounded p-2 mb-2"
          />
          <button
            onClick={handleScanUrl}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >Запустить по URL</button>
        </div>

        <div className="bg-white p-4 rounded shadow border">
          <label className="block font-medium mb-1">Загрузить swagger.yaml:</label>
          <input
            type="file"
            accept=".yaml,.yml"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            className="w-full mb-2"
          />
          <button
            onClick={handleScanSwagger}
            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
          >Запустить по Swagger</button>
        </div>

        {message && (
          <p className="text-center text-blue-700 font-medium mt-4">{message}</p>
        )}
      </div>
    </Layout>
  );
}