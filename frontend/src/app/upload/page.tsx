"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Navigation } from "@/components/shared/Navigation";
import { useAuth } from "@/lib/auth-context";

import {
  Upload,
  FileSpreadsheet,
  CheckCircle2,
  AlertCircle,
  ArrowLeft,
  Loader2,
} from "lucide-react";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();
  const { user, loading: authLoading } = useAuth();

  useEffect(() => {
    if (!authLoading && !user) {
      router.push("/login");
    }
  }, [user, authLoading, router]);

  if (authLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-emerald-600" />
      </div>
    );
  }

  if (!user) return null;
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      // Validate file type
      const validTypes = [".csv", ".xlsx", ".xls"];
      const fileExt = selectedFile.name
        .toLowerCase()
        .slice(selectedFile.name.lastIndexOf("."));

      if (!validTypes.includes(fileExt)) {
        setError("Please upload a CSV or Excel file");
        return;
      }

      // Validate file size (10MB limit)
      if (selectedFile.size > 10 * 1024 * 1024) {
        setError("File size must be less than 10MB");
        return;
      }

      setFile(selectedFile);
      setError(null);
      const reader = new FileReader();
      reader.onload = (e) => {
        if (e.target?.result) {
          localStorage.setItem("uploadedFileData", e.target.result as string);
        }
      };
      reader.readAsDataURL(selectedFile);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);
    setProgress(20);
    setError(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      setProgress(40);

      // Get auth token
      const token = localStorage.getItem("access_token");

      const response = await fetch("http://localhost:8000/api/v1/analyze", {
        method: "POST",
        body: formData,
        headers: token
          ? {
              Authorization: `Bearer ${token}`,
            }
          : {},
      });

      setProgress(70);

      if (response.ok) {
        const data = await response.json();
        setProgress(100);

        // Store results and file data
        localStorage.setItem("analysisResults", JSON.stringify(data));

        // Store original file for cleaning
        const reader = new FileReader();
        reader.onload = (e) => {
          if (e.target?.result) {
            localStorage.setItem("uploadedFileData", e.target.result as string);
            localStorage.setItem("originalFilename", file.name);
          }
        };
        reader.readAsDataURL(file);

        setTimeout(() => {
          router.push("/results");
        }, 500);
      } else {
        const errorData = await response.json();
        setError(errorData.detail || "Upload failed. Please try again.");
        setUploading(false);
        setProgress(0);
      }
    } catch (err) {
      console.error("Upload error:", err);
      setError(
        "Connection error. Make sure the backend is running on localhost:8000",
      );
      setUploading(false);
      setProgress(0);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />

      <div className="pt-32 pb-20 px-6">
        <div className="max-w-3xl mx-auto">
          {/* Back Button */}
          <Link
            href="/"
            className="inline-flex items-center text-sm text-gray-600 hover:text-gray-900 mb-8"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Home
          </Link>

          {/* Header */}
          <div className="text-center mb-10">
            <h1 className="text-4xl font-bold mb-3">Upload your file</h1>
            <p className="text-lg text-gray-600">
              Upload a CSV or Excel file to detect and fix data quality issues
            </p>
          </div>

          {/* Upload Card */}
          <Card className="p-8 border-2">
            {!file ? (
              <div className="border-2 border-dashed border-gray-300 rounded-xl p-16 text-center hover:border-emerald-500 transition-all cursor-pointer group">
                <label htmlFor="file-upload" className="cursor-pointer block">
                  <div className="w-16 h-16 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center group-hover:bg-emerald-50 transition-colors">
                    <Upload className="w-8 h-8 text-gray-400 group-hover:text-emerald-600 transition-colors" />
                  </div>
                  <p className="text-lg font-semibold mb-2 text-gray-900">
                    Click to upload or drag and drop
                  </p>
                  <p className="text-sm text-gray-500 mb-4">
                    CSV, XLSX, XLS files up to 10MB
                  </p>
                  <input
                    id="file-upload"
                    type="file"
                    className="hidden"
                    accept=".csv,.xlsx,.xls"
                    onChange={handleFileChange}
                  />
                </label>
              </div>
            ) : (
              <div className="space-y-6">
                {/* File Info */}
                <div className="flex items-center gap-4 p-4 bg-emerald-50 border border-emerald-200 rounded-lg">
                  <div className="w-12 h-12 bg-emerald-100 rounded-lg flex items-center justify-center flex-shrink-0">
                    <FileSpreadsheet className="w-6 h-6 text-emerald-700" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="font-medium text-gray-900 truncate">
                      {file.name}
                    </p>
                    <p className="text-sm text-gray-600">
                      {(file.size / 1024).toFixed(1)} KB ·{" "}
                      {file.type || "Unknown type"}
                    </p>
                  </div>
                  {!uploading && (
                    <CheckCircle2 className="w-6 h-6 text-emerald-600 flex-shrink-0" />
                  )}
                </div>

                {/* Progress Bar */}
                {uploading && (
                  <div className="space-y-3">
                    <Progress value={progress} className="h-2" />
                    <p className="text-center text-sm text-gray-600 font-medium">
                      {progress < 40 && "Uploading file..."}
                      {progress >= 40 &&
                        progress < 70 &&
                        "Analyzing with ML models..."}
                      {progress >= 70 &&
                        progress < 100 &&
                        "Generating report..."}
                      {progress === 100 && "Complete! Redirecting..."}
                    </p>
                  </div>
                )}

                {/* Error Message */}
                {error && (
                  <div className="flex items-start gap-3 p-4 bg-red-50 border border-red-200 rounded-lg">
                    <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
                    <div>
                      <p className="font-medium text-red-900">Upload failed</p>
                      <p className="text-sm text-red-700 mt-1">{error}</p>
                    </div>
                  </div>
                )}

                {/* Action Buttons */}
                {!uploading && (
                  <div className="flex gap-3">
                    <Button
                      onClick={handleUpload}
                      className="flex-1 h-12"
                      disabled={uploading}
                    >
                      Analyze File
                    </Button>
                    <Button
                      onClick={() => {
                        setFile(null);
                        setError(null);
                      }}
                      variant="outline"
                      className="h-12 px-6"
                    >
                      Remove
                    </Button>
                  </div>
                )}
              </div>
            )}
          </Card>

          {/* Security Notice */}
          <div className="mt-6 flex items-start gap-3 text-sm text-gray-600 bg-white p-4 rounded-lg border">
            <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5 text-gray-400" />
            <div>
              <p className="font-medium text-gray-900 mb-1">
                Your data is secure
              </p>
              <p>
                Files are processed securely and automatically deleted after 24
                hours. We never share or store your data permanently.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
