"use client";
import { useEffect, useState } from "react";
import API from "../../utils/api";
import { useRouter } from "next/navigation";
import { jwtDecode } from "jwt-decode";


export default function Projects() {
  const [projects, setProjects] = useState([]);
  const [users, setUsers] = useState([]);
  const [role, setRole] = useState("");
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      router.push("/");
      return;
    }
    const decoded = jwtDecode(token);
    setRole(decoded.role);
    API.get("/projects").then((res) => setProjects(res.data));
    if (decoded.role == "admin"){
      API.get("/auth/users").then((res) => setUsers(res.data)).catch(console.error);
    }
  }, []);

  return (
    <div>
      <h1>Projects</h1>
      {projects.map((p) => (
        <div key={p.id} onClick={() => router.push(`/tasks/${p.id}`)} style={{cursor: "pointer", padding: "10px", border: "1px solid #ccc", marginBottom: "5px", borderRadius: "5px"}}>
          {p.name}
        </div>
      ))}
    </div>
  );
}