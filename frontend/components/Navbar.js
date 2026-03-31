"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export default function Navbar() {
  const router = useRouter();
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token");
    setIsLoggedIn(!!token);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("token");
    setIsLoggedIn(false);
    router.push("/");
  };

  return (
    <nav
      style={{
        display: "flex",
        justifyContent: "space-between",
        padding: "10px 20px",
        background: "#eee",
      }}
    >
      <h3
        style={{ cursor: "pointer" }}
        onClick={() => router.push("/projects")}
      >
        Home
      </h3>

      {isLoggedIn && <button onClick={handleLogout}>Logout</button>}
    </nav>
  );
}