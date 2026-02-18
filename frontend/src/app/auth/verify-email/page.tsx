"use client";

import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { CheckCircle2, AlertCircle, Loader2 } from "lucide-react";
import Link from "next/link";

export default function VerifyEmailPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [status, setStatus] = useState<"loading" | "success" | "error">(
    "loading",
  );
  const [message, setMessage] = useState("");

  useEffect(() => {
    const token = searchParams.get("token");

    if (!token) {
      setStatus("error");
      setMessage("Invalid verification link");
      return;
    }

    verifyEmail(token);
  }, [searchParams]);

  const verifyEmail = async (token: string) => {
    try {
      const response = await fetch(
        `http://localhost:8000/api/v1/auth/verify-email?token=${token}`,
        { method: "POST" },
      );

      if (response.ok) {
        setStatus("success");
        setMessage("Email verified successfully! Redirecting...");

        // Redirect to login after 2 seconds
        setTimeout(() => {
          router.push("/login");
        }, 2000);
      } else {
        const data = await response.json();
        setStatus("error");
        setMessage(data.detail || "Verification failed");
      }
    } catch (error) {
      setStatus("error");
      setMessage("Network error. Please try again.");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center px-6">
      <Card className="p-8 max-w-md w-full text-center">
        {status === "loading" && (
          <>
            <Loader2 className="w-16 h-16 animate-spin mx-auto mb-4 text-emerald-600" />
            <h2 className="text-2xl font-bold mb-2">Verifying email...</h2>
            <p className="text-gray-600">Please wait</p>
          </>
        )}

        {status === "success" && (
          <>
            <div className="w-16 h-16 bg-emerald-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <CheckCircle2 className="w-10 h-10 text-emerald-600" />
            </div>
            <h2 className="text-2xl font-bold mb-2 text-emerald-900">
              Email Verified!
            </h2>
            <p className="text-gray-600 mb-6">{message}</p>
          </>
        )}

        {status === "error" && (
          <>
            <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <AlertCircle className="w-10 h-10 text-red-600" />
            </div>
            <h2 className="text-2xl font-bold mb-2 text-red-900">
              Verification Failed
            </h2>
            <p className="text-gray-600 mb-6">{message}</p>
            <Link href="/login">
              <Button className="w-full">Back to Login</Button>
            </Link>
          </>
        )}
      </Card>
    </div>
  );
}
