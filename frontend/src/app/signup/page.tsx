"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Sparkles, AlertCircle, Loader2, Check } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";

import { useAuth } from "@/lib/auth-context";
import { GoogleAuthButton } from "@/components/auth/GoogleAuthButton";
export default function SignupPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const { signup } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (password.length < 8) {
      setError("Password must be at least 8 characters");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch("http://localhost:8000/api/v1/auth/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email,
          password,
          full_name: fullName,
        }),
      });

      if (response.ok) {
        // Don't login automatically - show verification message
        router.push(`/auth/check-email?email=${encodeURIComponent(email)}`);
      } else {
        const data = await response.json();
        setError(data.detail || "Signup failed");
      }
    } catch (err: any) {
      setError(err.message || "Signup failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center px-6">
      <div className="w-full max-w-md">
        {/* Logo */}
        <Link href="/" className="flex items-center justify-center gap-2 mb-8">
          <div className="w-10 h-10 bg-gradient-to-br from-emerald-500 to-emerald-600 rounded-lg flex items-center justify-center">
            <Sparkles className="w-6 h-6 text-white" />
          </div>
          <span className="text-2xl font-bold">DataClean</span>
        </Link>

        <Card className="p-8 border-2">
          <div className="mb-6">
            <h1 className="text-2xl font-bold mb-2">Create your account</h1>
            <p className="text-gray-600">Start cleaning data for free</p>
          </div>
          {/* ✅ Google Signup */}
          <GoogleAuthButton mode="signup" />

          <div className="relative my-6">
            <div className="absolute inset-0 flex items-center">
              <span className="w-full border-t" />
            </div>
            <div className="relative flex justify-center text-xs uppercase">
              <span className="bg-white px-2 text-muted-foreground">
                Or continue with email
              </span>
            </div>
          </div>

          {/* Free Plan Benefits */}
          <div className="mb-6 p-4 bg-emerald-50 border border-emerald-200 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <Sparkles className="w-4 h-4 text-emerald-600" />
              <span className="font-medium text-sm text-emerald-900">
                Free Plan Includes:
              </span>
            </div>
            <ul className="space-y-1 text-sm text-emerald-700">
              <li className="flex items-center gap-2">
                <Check className="w-3 h-3" />
                <span>2 files per month</span>
              </li>
              <li className="flex items-center gap-2">
                <Check className="w-3 h-3" />
                <span>Up to 1,000 rows</span>
              </li>
              <li className="flex items-center gap-2">
                <Check className="w-3 h-3" />
                <span>ML-powered cleaning</span>
              </li>
            </ul>
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
                Full Name
              </label>
              <Input
                type="text"
                placeholder="John Doe"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                required
                disabled={loading}
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Email</label>
              <Input
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                disabled={loading}
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Password</label>
              <Input
                type="password"
                placeholder="Minimum 8 characters"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                minLength={8}
                disabled={loading}
              />
              <p className="text-xs text-gray-500 mt-1">
                Must be at least 8 characters
              </p>
            </div>

            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Creating account...
                </>
              ) : (
                "Create Account"
              )}
            </Button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600">
              Already have an account?{" "}
              <Link
                href="/login"
                className="text-emerald-600 hover:text-emerald-700 font-medium"
              >
                Sign in
              </Link>
            </p>
          </div>
        </Card>

        <p className="text-center text-sm text-gray-500 mt-6">
          By signing up, you agree to our Terms and Privacy Policy
        </p>
      </div>
    </div>
  );
}
