"use client";

import { useEffect, useState } from "react";
import API from "../../../utils/api";
import { useParams, useRouter } from "next/navigation";
import { jwtDecode } from "jwt-decode";

export default function Tasks() {
  const router = useRouter();
  const { id } = useParams();

  const [tasks, setTasks] = useState([]);
  const [role, setRole] = useState("");

  // ✅ Pagination state
  const [page, setPage] = useState(1);
  const limit = 5;

  /* ---------- ROLE ---------- */
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      const decoded = jwtDecode(token);
      setRole(decoded.role);
    }
  }, []);

  /* ---------- FETCH TASKS WITH PAGINATION ---------- */
  const fetchTasks = () => {
    const token = localStorage.getItem("token");
    if (!token) return; // ⛔ prevent request without token

    const offset = (page - 1) * limit;

    API.get(
      `/tasks?project_id=${Number(id)}&limit=${limit}&offset=${offset}`
    )
      .then((res) => setTasks(res.data))
      .catch(console.error);
  };

  /* ---------- LOAD DATA ---------- */
  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!id || !token) return;

    fetchTasks();
  }, [id, page]);
  /* ---------- STATUS COLOR ---------- */
  const statusColor = (status) => {
    switch (status) {
      case "pending":
        return "bg-yellow-100 text-yellow-700";
      case "in_progress":
        return "bg-blue-100 text-blue-700";
      case "done":
      case "completed":
        return "bg-green-100 text-green-700";
      case "cancelled":
        return "bg-red-100 text-red-700";
      default:
        return "bg-gray-100";
    }
  };

  return (
    <div className="p-8 bg-gray-100 min-h-screen">

      <h1 className="text-2xl font-bold mb-6">
        Project Tasks
      </h1>

      {/* ✅ CREATE BUTTON */}
      {(role === "admin" || role === "project_creator") && (
        <button
          onClick={() => router.push(`/tasks/create/${id}`)}
          className="bg-green-600 text-white px-4 py-2 rounded mb-4"
        >
          + Create Task
        </button>
      )}

      {/* ---------- TASK LIST ---------- */}
      <div className="grid gap-4">
        {tasks.map((t) => (
          <div
            key={t.id}
            className="bg-white p-4 rounded-xl shadow"
          >
            <h3 className="font-semibold">
              {t.title} -
              <span
                className={`ml-2 text-xs px-2 py-1 rounded ${statusColor(
                  t.status
                )}`}
              >
                - {t.status}
              </span>
            </h3>
          </div>
        ))}
      </div>

      {/* ---------- PAGINATION ---------- */}
      <div className="flex justify-center gap-4 mt-6">

        <button
          onClick={() => setPage((prev) => Math.max(prev - 1, 1))}
          disabled={page === 1}
          className="bg-gray-300 px-4 py-2 rounded disabled:opacity-50"
        >
          Previous
        </button>

        <span className="px-4 py-2 font-semibold">
          Page {page}
        </span>

        <button
          onClick={() => {
            if (tasks.length === limit) {
              setPage((prev) => prev + 1);
            }
          }}
          disabled={tasks.length < limit}
          className="bg-gray-300 px-4 py-2 rounded disabled:opacity-50"
        >
          Next
        </button>

      </div>

    </div>
  );
}