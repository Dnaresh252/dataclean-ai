"use client";

import { AlertCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useState } from "react";

interface VerificationBannerProps {
  email: string;
}

export function VerificationBanner({ email }: VerificationBannerProps) {
  const [resending, setResending] = useState(false);
  const [sent, setSent] = useState(false);

  const resendVerification = async () => {
    setResending(true);
    try {
      // TODO: Add resend endpoint
      await new Promise((resolve) => setTimeout(resolve, 1000));
      setSent(true);
    } catch (error) {
      console.error("Resend error:", error);
    } finally {
      setResending(false);
    }
  };

  return (
    <div className="bg-amber-50 border-b border-amber-200 px-6 py-3">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <div className="flex items-center gap-3">
          <AlertCircle className="w-5 h-5 text-amber-600" />
          <div>
            <span className="text-sm font-medium text-amber-900">
              Please verify your email address
            </span>
            <span className="text-sm text-amber-700 ml-2">
              We sent a verification link to {email}
            </span>
          </div>
        </div>
        <Button
          size="sm"
          variant="outline"
          onClick={resendVerification}
          disabled={resending || sent}
          className="border-amber-300 hover:bg-amber-100"
        >
          {sent ? "Email sent!" : resending ? "Sending..." : "Resend email"}
        </Button>
      </div>
    </div>
  );
}
