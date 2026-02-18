"use client";

import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Loader2, AlertCircle } from "lucide-react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { useAuth } from "@/lib/auth-context";

export default function GoogleCallbackPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const code = searchParams.get("code");

    if (!code) {
      setError("No authorization code received from Google");
      return;
    }

    handleGoogleCallback(code);
  }, [searchParams]);

  const handleGoogleCallback = async (code: string) => {
    try {
      // Send code to backend
      const response = await fetch(
        `http://localhost:8000/api/v1/auth/google/callback?code=${encodeURIComponent(code)}`,
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Authentication failed");
      }

      const data = await response.json();

      // Save token
      localStorage.setItem("access_token", data.access_token);

      // Small delay to ensure storage is complete
      await new Promise((resolve) => setTimeout(resolve, 100));

      // Force reload to update auth context
      window.location.href = "/dashboard";
    } catch (err: any) {
      console.error("Google callback error:", err);
      setError(err.message || "Authentication failed");
    }
  };

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center px-6">
        <Card className="p-8 max-w-md w-full">
          <div className="flex items-start gap-3 mb-6">
            <AlertCircle className="w-6 h-6 text-red-600 flex-shrink-0 mt-0.5" />
            <div>
              <h2 className="text-lg font-semibold text-red-900 mb-1">
                Authentication Failed
              </h2>
              <p className="text-sm text-red-700">{error}</p>
            </div>
          </div>
          <Link href="/login">
            <Button className="w-full">Back to Login</Button>
          </Link>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-6">
      <Card className="p-8 max-w-md w-full text-center">
        <Loader2 className="w-12 h-12 animate-spin mx-auto mb-4 text-emerald-600" />
        <h2 className="text-xl font-semibold mb-2">Signing you in...</h2>
        <p className="text-gray-600">Redirecting to dashboard...</p>
      </Card>
    </div>
  );
}
