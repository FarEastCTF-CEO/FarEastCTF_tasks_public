// src/components/Layout.tsx
import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
export default function Layout({ children }: { children: React.ReactNode }) {
  const { logout, role } = useAuth();
let navigate = useNavigate(); 
  const loginRoute = () =>{ 
    let path = `/login`; 
    navigate(path);
  }
  const registerRoute = () =>{ 
    let path = `/register`; 
    navigate(path);
  }
  const logoutRoute = () =>{
    let path = `/login`
    navigate(path)
  }
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow p-4 flex justify-between items-center">
        <div className="flex gap-4 items-center">
          <Link to="/dashboard" className="text-lg font-semibold text-blue-700">ScannerApp</Link>
          {role !== null && (
          <Link to="/scan" className="text-gray-700 hover:text-blue-600">Сканировать</Link>
          )}
          {role === "admin" && (
            <Link to="/admin" className="text-gray-700 hover:text-blue-600">Админ</Link>
          )}
        </div>
        <div className="flex gap-4 items-center">
        {role === null &&( <button
          onClick={loginRoute}
          className="text-sm text-white bg-blue-500 px-3 py-1 rounded hover:bg-blue-600"
        >Логин</button>
        )}
        {role === null &&( <button
          onClick={registerRoute}
          className="text-sm text-white bg-green-500 px-3 py-1 rounded hover:bg-green-600"
        >Регистрация</button>
        )}
        {role !== null &&( <button
          onClick={logoutRoute}
          className="text-sm text-white bg-red-500 px-3 py-1 rounded hover:bg-red-600"
        >Выйти</button>)}
        </div>
      </header>
      <main className="p-6 max-w-5xl mx-auto">
        {children}
      </main>
    </div>
  );
}
