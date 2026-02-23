// src/pages/AdminPanel.tsx
import React, { useEffect, useState } from "react";
import axios from "axios";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import Layout from "../components/Layout";
const apiUrl = import.meta.env.VITE_API_URL;

interface User {
  id: number;
  username: string;
  role: string;
}

export default function AdminPanel() {
  const [users, setUsers] = useState<User[]>([]);
  const [error, setError] = useState("");
  const { logout, role } = useAuth();
  const navigate = useNavigate();

  const fetchUsers = async () => {
    try {
      const res = await axios.get(`${apiUrl}/api/users`);
      setUsers(res.data);
    } catch {
      setError("Недостаточно прав или ошибка запроса");
    }
  };

  const updateRole = async (id: number, newRole: string) => {
    try {
      await axios.post(`${apiUrl}/api/user/${id}/role`, { role: newRole });
      fetchUsers();
    } catch {
      alert("Ошибка обновления роли");
    }
  };

  useEffect(() => {
    if (role !== "admin") {
      navigate("/dashboard");
    } else {
      fetchUsers();
    }
  }, [role]);

  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-6">Панель администратора</h1>
      {error && <p className="text-red-600 mb-4">{error}</p>}

      <div className="overflow-x-auto">
        <table className="w-full text-sm border">
          <thead>
            <tr className="bg-gray-100 text-left">
              <th className="p-2 border">ID</th>
              <th className="p-2 border">Пользователь</th>
              <th className="p-2 border">Роль</th>
              <th className="p-2 border">Действие</th>
            </tr>
          </thead>
          <tbody>
            {users.map(user => (
              <tr key={user.id} className="text-center bg-white border-t">
                <td className="p-2 border">{user.id}</td>
                <td className="p-2 border">{user.username}</td>
                <td className="p-2 border">
                  <span className={`px-2 py-1 rounded text-white text-xs ${user.role === "admin" ? "bg-orange-500" : "bg-gray-500"}`}>
                    {user.role}
                  </span>
                </td>
                <td className="p-2 border">
                  {user.role !== "admin" ? (
                    <button
                      className="bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700"
                      onClick={() => updateRole(user.id, "admin")}
                    >Сделать админом</button>
                  ) : (
                    <button
                      className="bg-gray-500 text-white px-3 py-1 rounded hover:bg-gray-600"
                      onClick={() => updateRole(user.id, "user")}
                    >Сделать обычным</button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Layout>
  );
}
