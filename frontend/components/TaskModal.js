import { useState } from "react";
import API from "../utils/api";

export default function TaskModal({ projectId, refresh }) {
  const [title, setTitle] = useState("");

  const createTask = async () => {
    await API.post("/tasks", {
      title,
      project_id: projectId,
    });
    refresh();
  };

  return (
    <div>
      <input onChange={(e) => setTitle(e.target.value)} />
      <button onClick={createTask}>Create</button>
    </div>
  );
}