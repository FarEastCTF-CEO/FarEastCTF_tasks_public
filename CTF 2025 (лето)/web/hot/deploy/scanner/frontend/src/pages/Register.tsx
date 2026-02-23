// src/pages/Register.tsx
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import Layout from "../components/Layout";
const apiUrl = import.meta.env.VITE_API_URL;

export default function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await axios.post(`${apiUrl}/register`, {username, password}, {headers: {'Content-Type': 'application/json'}, withCredentials: true});
      setSuccess(true);
      setTimeout(() => navigate("/login"), 1500);
    } catch (err) {
      setError("Ошибка регистрации. Возможно, пользователь уже существует.");
    }
  };

  return (
    <Layout>
      <div className="flex items-center justify-center min-h-[70vh]">
        <form onSubmit={handleSubmit} className="bg-white p-8 rounded-xl shadow-md w-full max-w-sm">
          <h2 className="text-2xl mb-4 text-center font-semibold">Регистрация</h2>
          {error && <p className="text-red-500 mb-3 text-sm text-center">{error}</p>}
          {success && <p className="text-green-600 mb-3 text-sm text-center">Успешно! Переход к входу...</p>}
          <input
            type="text"
            placeholder="Имя пользователя"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="w-full border p-2 mb-4 rounded"
            required
          />
          <input
            type="password"
            placeholder="Пароль"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full border p-2 mb-4 rounded"
            required
          />
          <button
            type="submit"
            className="w-full bg-green-600 text-white p-2 rounded hover:bg-green-700"
          >
            Зарегистрироваться
          </button>
        </form>
      </div>
    </Layout>
  );
}
