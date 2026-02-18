"use client";

import { useEffect, useState } from "react";
import { Navigation } from "@/components/shared/Navigation";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import {
  Upload,
  FileSpreadsheet,
  TrendingUp,
  Clock,
  AlertCircle,
  ArrowRight,
  Loader2,
} from "lucide-react";
import Link from "next/link";
import { useAuth } from "@/lib/auth-context";
import { useRouter } from "next/navigation";

interface UsageData {
  files_analyzed: number;
  rows_processed: number;
  plan: string;
  limit_files: number;
  limit_rows: number;
}

interface FileHistory {
  id: string;
  original_filename: string;
  rows_count: number;
  problems_detected: number;
  status: string;
  uploaded_at: string;
}

export default function DashboardPage() {
  const { user, loading } = useAuth();
  const router = useRouter();
  const [usage, setUsage] = useState<UsageData | null>(null);
  const [files, setFiles] = useState<FileHistory[]>([]);
  const [loadingData, setLoadingData] = useState(true);

  useEffect(() => {
    if (!loading && !user) {
      router.push("/login");
    } else if (user) {
      fetchDashboardData();
    }
  }, [user, loading, router]);

  const fetchDashboardData = async () => {
    const token = localStorage.getItem("access_token");
    if (!token) return;

    try {
      // Fetch usage stats
      const usageRes = await fetch("http://localhost:8000/api/v1/auth/usage", {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (usageRes.ok) {
        const usageData = await usageRes.json();
        setUsage(usageData);
      }

      // Fetch file history
      const filesRes = await fetch("http://localhost:8000/api/v1/files", {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (filesRes.ok) {
        const filesData = await filesRes.json();
        setFiles(filesData.files || []);
      }
    } catch (error) {
      console.error("Error fetching dashboard data:", error);
    } finally {
      setLoadingData(false);
    }
  };
  if (loading || loadingData) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-8 h-8 animate-spin mx-auto mb-4 text-emerald-600" />
          <p className="text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (!user) return null;

  const usagePercentage = usage
    ? (usage.files_analyzed / usage.limit_files) * 100
    : 0;

  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />

      <div className="pt-32 pb-20 px-6">
        <div className="max-w-7xl mx-auto">
          {/* Welcome Header */}
          <div className="mb-10">
            <h1 className="text-4xl font-bold mb-2">
              Welcome back, {user.full_name?.split(" ")[0] || "there"}!
            </h1>
            <p className="text-lg text-gray-600">
              Here's your data cleaning activity
            </p>
          </div>

          {/* Stats Cards */}
          <div className="grid md:grid-cols-4 gap-6 mb-10">
            <Card className="p-6 border-2">
              <div className="flex items-center justify-between mb-4">
                <FileSpreadsheet className="w-8 h-8 text-emerald-600" />
                <Badge variant="secondary">{user.plan.toUpperCase()}</Badge>
              </div>
              <div className="text-3xl font-bold mb-1">
                {usage?.files_analyzed || 0}
              </div>
              <div className="text-sm text-gray-600">
                Files cleaned this month
              </div>
            </Card>

            <Card className="p-6 border-2">
              <TrendingUp className="w-8 h-8 text-blue-600 mb-4" />
              <div className="text-3xl font-bold mb-1">
                {usage?.rows_processed.toLocaleString() || 0}
              </div>
              <div className="text-sm text-gray-600">Rows processed</div>
            </Card>

            <Card className="p-6 border-2">
              <Clock className="w-8 h-8 text-purple-600 mb-4" />
              <div className="text-3xl font-bold mb-1">
                ~{((usage?.files_analyzed || 0) * 2).toFixed(0)}h
              </div>
              <div className="text-sm text-gray-600">Time saved</div>
            </Card>

            <Card className="p-6 border-2 bg-emerald-50 border-emerald-200">
              <div className="text-sm font-medium text-emerald-700 mb-2">
                Usage this month
              </div>
              <Progress value={usagePercentage} className="h-2 mb-2" />
              <div className="text-sm text-emerald-700">
                {usage?.files_analyzed || 0} / {usage?.limit_files || 2} files
              </div>
            </Card>
          </div>

          {/* Quick Actions */}
          <div className="grid md:grid-cols-2 gap-6 mb-10">
            <Card className="p-8 border-2 hover:border-emerald-200 transition-colors">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="text-xl font-semibold mb-2">
                    Upload New File
                  </h3>
                  <p className="text-gray-600">
                    Clean a CSV or Excel file with ML-powered detection
                  </p>
                </div>
                <Upload className="w-8 h-8 text-emerald-600" />
              </div>
              <Link href="/upload">
                <Button className="w-full">
                  Upload File
                  <ArrowRight className="ml-2 w-4 h-4" />
                </Button>
              </Link>
            </Card>

            <Card className="p-8 border-2">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="text-xl font-semibold mb-2">Upgrade to Pro</h3>
                  <p className="text-gray-600">
                    50 files/month • 10K rows • API access
                  </p>
                </div>
                <TrendingUp className="w-8 h-8 text-blue-600" />
              </div>
              <Button variant="outline" className="w-full" disabled>
                ₹499/month • Coming Soon
              </Button>
            </Card>
          </div>

          {/* File History */}
          <Card className="p-8 border-2">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold">Recent Files</h2>
              <Badge variant="outline">Last 30 days</Badge>
            </div>

            {files.length === 0 ? (
              <div className="text-center py-12">
                <FileSpreadsheet className="w-16 h-16 mx-auto mb-4 text-gray-300" />
                <h3 className="text-lg font-semibold mb-2">No files yet</h3>
                <p className="text-gray-600 mb-6">
                  Upload your first file to see it here
                </p>
                <Link href="/upload">
                  <Button>
                    <Upload className="mr-2 w-4 h-4" />
                    Upload First File
                  </Button>
                </Link>
              </div>
            ) : (
              <div className="space-y-3">
                {files.map((file) => (
                  <div
                    key={file.id}
                    className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                  >
                    <div className="flex items-center gap-4">
                      <FileSpreadsheet className="w-8 h-8 text-gray-400" />
                      <div>
                        <div className="font-medium">
                          {file.original_filename}
                        </div>
                        <div className="text-sm text-gray-600">
                          {file.rows_count.toLocaleString()} rows •{" "}
                          {file.problems_detected} issues
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center gap-3">
                      <Badge>{file.status}</Badge>
                      <span className="text-sm text-gray-500">
                        {new Date(file.uploaded_at).toLocaleDateString()}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </Card>

          {/* Usage Warning */}
          {usage && usage.files_analyzed >= usage.limit_files && (
            <div className="mt-6 p-4 bg-amber-50 border border-amber-200 rounded-lg flex items-start gap-3">
              <AlertCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
              <div>
                <div className="font-medium text-amber-900">
                  Monthly limit reached
                </div>
                <p className="text-sm text-amber-700 mt-1">
                  You've used all {usage.limit_files} free files this month.
                  Upgrade to Pro for 50 files/month.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
