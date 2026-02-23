import React, { useEffect, useState } from "react";
import axios from "axios";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import Layout from "../components/Layout";
const apiUrl = import.meta.env.VITE_API_URL;

interface Scan {
  id: number;
  method: string;
  url: string;
  response: string;
  created_at: string;
  status: string;
  params?: string;
}

interface ScanGroup {
  host: string;
  created_at: string;
  scans: Scan[];
}
const waitForPDF = async (url: string, timeout = 10000) => {
  const start = Date.now();

  while (Date.now() - start < timeout) {
    try {
      const res = await axios.head(url);
      if (res.status === 200) return true;
    } catch (_) {
      // ignore
    }
    await new Promise(r => setTimeout(r, 500));
  }

  throw new Error("PDF файл не появился вовремя");
};

const generateReport = async (host: string, scans: Scan[]) => {
  const html = `
    <html>
      <head><title>Отчёт по ${host}</title></head>
      <body>
        <h1>Отчёт по ${host}</h1>
        <ul>
          ${scans.map(scan => `
            <li>
              <strong>${scan.method}</strong> ${scan.url}<br/>
              <pre>${scan.response}</pre>
            </li>
          `).join("")}
        </ul>
      </body>
    </html>
  `;

  try {
    const token = localStorage.getItem("token");
    const res = await axios.post(`${apiUrl}/api/generate-report`, {host, html}, {
      headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}` }
    });
    if (res.data?.url) {
          await waitForPDF(`${apiUrl}${res.data.url}`);

      const fileRes = await axios.get(`${apiUrl}${res.data.url}`, {
        responseType: "blob"
      });

      // Создаём ссылку на blob и скачиваем
      const url = window.URL.createObjectURL(new Blob([fileRes.data], { type: "application/pdf" }));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", `report-${host}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } else {
      alert("Не удалось получить ссылку на отчёт.");
    }
  } catch (err) {
    console.error("Ошибка при генерации отчёта:", err);
    alert("Ошибка при генерации отчёта");
  }
};

function groupScansByHostAndTime(scans: Scan[]): ScanGroup[] {
  const groups: { [key: string]: ScanGroup } = {};

  scans.forEach((scan) => {
    try {
      const normalized = scan.url.startsWith("http") ? scan.url : `http://${scan.url}`;
      const url = new URL(normalized);
      const host = url.host;
      const time = new Date(scan.created_at).toISOString().slice(0, 16); // group by minute
      const key = `${host}-${time}`;

      if (!groups[key]) {
        groups[key] = {
          host,
          created_at: time,
          scans: [],
        };
      }

      groups[key].scans.push(scan);
    } catch (e) {
      console.error("Invalid URL in scan:", scan.url);
    }
  });

  return Object.values(groups).sort((a, b) => (a.created_at < b.created_at ? 1 : -1));
}

export default function Dashboard() {
  const [scans, setScans] = useState<Scan[]>([]);
  const { logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      console.warn("Нет токена, вызываем logout()");
      logout();
      return;
    }

    const fetchScans = () => {
      axios.get(`${apiUrl}/api/scans`, {
        headers: { Authorization: `Bearer ${token}` }
      })
        .then(res => {
          console.log("Получены сканы:", res.data);
          setScans(Array.isArray(res.data) ? res.data : []);
        })
        .catch((err) => {
          if (err.response?.status === 401) {
            console.warn("Unauthorized, вызываем logout()");
            logout();
          } else {
            console.error("Ошибка при получении сканирований:", err);
          }
        });
    };

    fetchScans();
    const intervalId = setInterval(fetchScans, 5000); // обновлять каждые 5 секунд
    return () => clearInterval(intervalId);
  }, [logout]);

  const grouped = groupScansByHostAndTime(scans);

  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-6">История сканирований</h1>
      {grouped.length === 0 ? (
        <p className="text-gray-500">Сканирования пока не выполнялись.</p>
      ) : (
        <div className="space-y-8">
          {grouped.map((group, i) => (
            <div key={i} className="border rounded-xl p-4 bg-white shadow">
              <div className="flex justify-between items-center mb-3">
                <h2 className="text-lg font-semibold">
                  Хост: {group.host} — {new Date(group.created_at).toLocaleString()}
                </h2>
                <button
                  className="bg-blue-600 hover:bg-blue-700 text-white text-sm px-4 py-1 rounded"
                  onClick={() =>{ 
                    const completedScans = group.scans.filter(s => s.status === "done");
                    if (completedScans.length === 0) {
                      alert("Нет завершённых сканирований для отчёта");
                      return;
                    }
                    generateReport(group.host, group.scans);}}
                >
                  Сгенерировать отчёт
                </button>
              </div>
              <div className="space-y-3">
                {group.scans.map(scan => (
                  <div key={scan.id} className="border rounded p-3">
                    <div className="flex justify-between items-center mb-1">
                      <div>
                        <span className="text-sm font-mono text-blue-600">{scan.method} {scan.url}</span>
                        <span className="text-xs font-medium text-gray-500 ml-2">
                          Статус: {" "}
                          <span
                            className={
                              scan.status === "done"
                                ? "text-green-600"
                                : scan.status === "error"
                                  ? "text-red-600"
                                  : "text-yellow-600"
                            }
                          >
                            {scan.status}
                          </span>
                        </span>
                      </div>
                      <span className="text-xs text-gray-500">{new Date(scan.created_at).toLocaleTimeString()}</span>
                    </div>
                    {scan.params && (
                      <div className="text-xs text-gray-700 mb-2">
                        Параметры: <code className="font-mono">{scan.params}</code>
                      </div>
                    )}
                    <pre className="bg-gray-100 text-sm p-2 rounded overflow-auto max-h-48 whitespace-pre-wrap">
                      {scan.response.slice(0, 1000)}
                    </pre>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </Layout>
  );
}
