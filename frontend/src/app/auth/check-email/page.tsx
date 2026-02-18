"use client";

import { useSearchParams } from "next/navigation";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Mail, CheckCircle } from "lucide-react";
import Link from "next/link";

export default function CheckEmailPage() {
  const searchParams = useSearchParams();
  const email = searchParams.get("email") || "your email";

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center px-6">
      <Card className="p-8 max-w-md w-full text-center">
        <div className="w-16 h-16 bg-emerald-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <Mail className="w-10 h-10 text-emerald-600" />
        </div>

        <h1 className="text-2xl font-bold mb-2">Check your email</h1>

        <p className="text-gray-600 mb-6">
          We sent a verification link to <strong>{email}</strong>
        </p>

        <div className="bg-emerald-50 border border-emerald-200 rounded-lg p-4 mb-6">
          <div className="flex items-start gap-3">
            <CheckCircle className="w-5 h-5 text-emerald-600 flex-shrink-0 mt-0.5" />
            <div className="text-left text-sm">
              <p className="font-medium text-emerald-900 mb-1">Next steps:</p>
              <ol className="list-decimal list-inside space-y-1 text-emerald-700">
                <li>Check your inbox (and spam folder)</li>
                <li>Click the verification link</li>
                <li>Start cleaning your data!</li>
              </ol>
            </div>
          </div>
        </div>

        <div className="space-y-3">
          <p className="text-sm text-gray-600">Didn't receive the email?</p>
          <Button variant="outline" className="w-full" disabled>
            Resend verification email
          </Button>

          <Link href="/login" className="block">
            <Button variant="ghost" className="w-full">
              Back to Login
            </Button>
          </Link>
        </div>
      </Card>
    </div>
  );
}
