// src/context/AuthContext.tsx
import React, { createContext, useContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
const apiUrl = import.meta.env.VITE_API_URL;


interface AuthContextType {
  token: string | null;
  role: string | null;
  login: (username: string, password: string) => Promise<boolean>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType>({
  token: null,
  role: null,
  login: async () => false,
  logout: () => {},
});

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [token, setToken] = useState<string | null>(null);
  const [role, setRole] = useState<string | null>(null);

  // Загружаем из localStorage при инициализации
  useEffect(() => {
    const savedToken = localStorage.getItem("token");
    const savedRole = localStorage.getItem("role");
    if (savedToken) setToken(savedToken);
    if (savedRole) setRole(savedRole);
  }, []);

  // Устанавливаем axios заголовок авторизации
  useEffect(() => {
    if (token) {
      axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
    } else {
      delete axios.defaults.headers.common["Authorization"];
    }
  }, [token]);

  const login = async (username: string, password: string) => {
    try {
      const res = await axios.post(`${apiUrl}/login`, { username, password }, {
        headers: { 'Content-Type': 'application/json' }
      });


      if (res.data.token) {
        const payload = JSON.parse(atob(res.data.token.split(".")[1]));

        setToken(res.data.token);
        setRole(payload.role);

        // Явно сохраняем до возможного navigate()
        localStorage.setItem("token", res.data.token);
        localStorage.setItem("role", payload.role);

        return true;
      }
    } catch (err) {
      console.error("Login failed", err);
    }
    return false;
  };

  const logout = () => {
    setToken(null);
    setRole(null);
    localStorage.removeItem("token");
    localStorage.removeItem("role");
  };

  return (
    <AuthContext.Provider value={{ token, role, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
