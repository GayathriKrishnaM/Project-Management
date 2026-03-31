"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import API from "../../../../utils/api";

export default function CreateTask() {
  const { id } = useParams();
  const router = useRouter();

  const [users, setUsers] = useState([]);

  const [task, setTask] = useState({
    title: "",
    description: "",
    assigned_to: null,
    status: "pending",   // ✅ default value
    due_date: ""
  });

  /* ---------- FETCH USERS ---------- */
  useEffect(() => {
    API.get("/auth/users")
      .then((res) =>
        setUsers(res.data.filter(u => u.role !== "admin"))
      )
      .catch(console.error);
  }, []);

  /* ---------- CREATE TASK ---------- */
  const handleCreate = async () => {
    if (!task.title.trim()) {
      alert("Title is required");
      return;
    }

    try {
      await API.post("/tasks", {
        title: task.title,
        project_id: Number(id),
        description: task.description || null,
        status: task.status,
        due_date: task.due_date || null,
        assigned_to: task.assigned_to
          ? Number(task.assigned_to)
          : null,
      });

      // ✅ REDIRECT AFTER SUCCESS
      router.push(`/tasks/${id}`);

    } catch (err) {
      console.error(err.response?.data);
    }
  };

  return (
    <div className="p-8">

      <h1 className="text-2xl font-bold mb-6">
        Create Task
      </h1>

      <div className="flex flex-col gap-3 max-w-md">

        {/* TITLE */}
        <input
          className="border p-2 rounded"
          placeholder="Title"
          value={task.title}
          onChange={(e) =>
            setTask({ ...task, title: e.target.value })
          }
        />

        {/* DESCRIPTION */}
        <input
          className="border p-2 rounded"
          placeholder="Description"
          value={task.description}
          onChange={(e) =>
            setTask({ ...task, description: e.target.value })
          }
        />

        {/* DUE DATE */}
        <input
          type="date"
          className="border p-2 rounded"
          value={task.due_date || ""}
          onChange={(e) =>
            setTask({
              ...task,
              due_date: e.target.value || null
            })
          }
        />

        {/* ✅ STATUS DROPDOWN */}
        <select
          className="border p-2 rounded"
          value={task.status}
          onChange={(e) =>
            setTask({ ...task, status: e.target.value })
          }
        >
          <option value="pending">Pending</option>
          <option value="in_progress">In Progress</option>
          <option value="done">Done</option>
          <option value="completed">Completed</option>
          <option value="cancelled">Cancelled</option>
        </select>

        {/* USERS */}
        <select
          className="border p-2 rounded"
          value={task.assigned_to ?? ""}
          onChange={(e) =>
            setTask({
              ...task,
              assigned_to: e.target.value || null
            })
          }
        >
          <option value="">Unassigned</option>
          {users.map((u) => (
            <option key={u.id} value={u.id}>
              {u.name}
            </option>
          ))}
        </select>

        {/* BUTTON */}
        <button
          onClick={handleCreate}
          className="bg-blue-600 text-white p-2 rounded"
        >
          Create Task
        </button>

      </div>
    </div>
  );
}