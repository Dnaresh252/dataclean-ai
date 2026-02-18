"use client";

import { useState, useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Sparkles, AlertCircle, CheckCircle2, Loader2 } from "lucide-react";
import Link from "next/link";

export default function ResetPasswordPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState("");
  const [token, setToken] = useState("");

  useEffect(() => {
    const tokenParam = searchParams.get("token");
    if (!tokenParam) {
      setError("Invalid reset link");
    } else {
      setToken(tokenParam);
    }
  }, [searchParams]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (password.length < 8) {
      setError("Password must be at least 8 characters");
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(
        "http://localhost:8000/api/v1/auth/reset-password",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ token, new_password: password }),
        },
      );

      if (response.ok) {
        setSuccess(true);
        setTimeout(() => router.push("/login"), 2000);
      } else {
        const data = await response.json();
        setError(data.detail || "Failed to reset password");
      }
    } catch (err) {
      setError("Network error. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center px-6">
      <div className="w-full max-w-md">
        <Link href="/" className="flex items-center justify-center gap-2 mb-8">
          <div className="w-10 h-10 bg-gradient-to-br from-emerald-500 to-emerald-600 rounded-lg flex items-center justify-center">
            <Sparkles className="w-6 h-6 text-white" />
          </div>
          <span className="text-2xl font-bold">DataClean</span>
        </Link>

        <Card className="p-8 border-2">
          {!success ? (
            <>
              <div className="mb-6">
                <h1 className="text-2xl font-bold mb-2">Reset your password</h1>
                <p className="text-gray-600">Enter your new password below</p>
              </div>

              {error && (
                <div className="mb-6 p-3 bg-red-50 border border-red-200 rounded-lg flex items-start gap-2">
                  <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
                  <p className="text-sm text-red-700">{error}</p>
                </div>
              )}

              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-2">
                    New Password
                  </label>
                  <Input
                    type="password"
                    placeholder="Minimum 8 characters"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    minLength={8}
                    disabled={loading || !token}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">
                    Confirm Password
                  </label>
                  <Input
                    type="password"
                    placeholder="Re-enter password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    required
                    minLength={8}
                    disabled={loading || !token}
                  />
                </div>

                <Button
                  type="submit"
                  className="w-full"
                  disabled={loading || !token}
                >
                  {loading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Resetting...
                    </>
                  ) : (
                    "Reset Password"
                  )}
                </Button>
              </form>
            </>
          ) : (
            <div className="text-center py-4">
              <div className="w-16 h-16 bg-emerald-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <CheckCircle2 className="w-10 h-10 text-emerald-600" />
              </div>
              <h2 className="text-2xl font-bold mb-2">Password reset!</h2>
              <p className="text-gray-600">Redirecting to login...</p>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}
