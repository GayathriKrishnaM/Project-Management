"use client";

import { useState } from "react";
import API from "../utils/api";
import { useRouter } from "next/navigation";

export default function Login() {
const [email, setEmail] = useState("");
const [otp, setOtp] = useState("");
const [otpToken, setOtpToken] = useState("");
const [step, setStep] = useState(1); // 1 = email, 2 = otp
const [loading, setLoading] = useState(false);
const [error, setError] = useState("");

const router = useRouter();

// Step 1 → Request OTP
const handleRequestOTP = async () => {
try {
setLoading(true);
setError("");

  const res = await API.post("/auth/request-login", null, {
    params: { email }, // since backend expects query param
  });

  setOtpToken(res.data.otp_token);
  setStep(2); // move to OTP screen
} catch (err) {
  setError("User not found or error sending OTP");
} finally {
  setLoading(false);
}

};

// Step 2 → Verify OTP
const handleVerifyOTP = async () => {
try {
setLoading(true);
setError("");

  const res = await API.post("/auth/verify-login", null, {
    params: {
      email,
      otp,
      otp_token: otpToken,
    },
  });

  localStorage.setItem("token", res.data.access_token);

  router.push("/projects");
} catch (err) {
  setError("Invalid OTP");
} finally {
  setLoading(false);
}

};

return ( <div className="min-h-screen flex items-center justify-center bg-gray-100"> <div className="bg-white shadow-xl rounded-2xl p-8 w-full max-w-md">

    <h1 className="text-2xl font-bold text-center mb-6">
      Login with OTP
    </h1>

    {error && (
      <div className="bg-red-100 text-red-600 p-2 rounded mb-4 text-sm">
        {error}
      </div>
    )}

    {/* STEP 1: EMAIL */}
    {step === 1 && (
      <>
        <input
          className="w-full border rounded-lg p-3 mb-4"
          placeholder="Enter Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <button
          onClick={handleRequestOTP}
          disabled={loading}
          className="w-full bg-blue-600 text-white p-3 rounded-lg"
        >
          {loading ? "Sending OTP..." : "Send OTP"}
        </button>
      </>
    )}

    {/* STEP 2: OTP */}
    {step === 2 && (
      <>
        <input
          className="w-full border rounded-lg p-3 mb-4"
          placeholder="Enter OTP"
          value={otp}
          onChange={(e) => setOtp(e.target.value)}
        />

        <button
          onClick={handleVerifyOTP}
          disabled={loading}
          className="w-full bg-green-600 text-white p-3 rounded-lg"
        >
          {loading ? "Verifying..." : "Verify OTP"}
        </button>
      </>
    )}
  </div>
</div>
);
}
