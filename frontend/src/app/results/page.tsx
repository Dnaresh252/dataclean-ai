"use client";

import { useEffect, useState } from "react";
import { Navigation } from "@/components/shared/Navigation";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import {
  Download,
  AlertCircle,
  CheckCircle2,
  FileSpreadsheet,
  TrendingDown,
  ArrowLeft,
} from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";

interface AnalysisData {
  filename: string;
  file_info: {
    rows: number;
    columns: number;
  };
  problems_detected: Array<{
    column: string;
    problem_type: string;
    probability: number;
  }>;
  recommendations: Array<{
    operation: string;
    column?: string;
    priority: string;
    reason: string;
  }>;
  summary: {
    total_problems: number;
    recommended_operations: number;
  };
}

export default function ResultsPage() {
  const [analysisData, setAnalysisData] = useState<AnalysisData | null>(null);
  const [downloading, setDownloading] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const data = localStorage.getItem("analysisResults");
    if (data) {
      setAnalysisData(JSON.parse(data));
    } else {
      router.push("/upload");
    }
  }, [router]);

  const handleDownloadClean = async () => {
    if (!analysisData) return;

    setDownloading(true);

    try {
      // Get original file from localStorage
      const originalFilename = localStorage.getItem("originalFilename");
      const originalFileData = localStorage.getItem("uploadedFileData");

      if (!originalFileData) {
        alert("Original file not found. Please upload again.");
        router.push("/upload");
        return;
      }

      // Convert base64 back to file
      const base64Response = await fetch(originalFileData);
      const blob = await base64Response.blob();

      const formData = new FormData();
      formData.append("file", blob, originalFilename || "file.csv");

      const response = await fetch("http://localhost:8000/api/v1/clean", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const cleanedBlob = await response.blob();
        const url = window.URL.createObjectURL(cleanedBlob);
        const a = document.createElement("a");
        a.href = url;
        const cleanFilename = (
          originalFilename || analysisData.filename
        ).replace(/\.[^/.]+$/, "_cleaned.csv");
        a.download = cleanFilename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        alert("✅ File cleaned successfully!");
      } else {
        const errorData = await response.json();
        alert(`Failed: ${errorData.detail || "Unknown error"}`);
      }
    } catch (error) {
      console.error("Download error:", error);
      alert(
        "Error downloading file. Make sure backend is running on localhost:8000",
      );
    } finally {
      setDownloading(false);
    }
  };

  if (!analysisData) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin w-8 h-8 border-4 border-emerald-600 border-t-transparent rounded-full mx-auto mb-4" />
          <p className="text-gray-600">Loading results...</p>
        </div>
      </div>
    );
  }

  const problemsByPriority = {
    high: analysisData.recommendations.filter((r) => r.priority === "high")
      .length,
    medium: analysisData.recommendations.filter((r) => r.priority === "medium")
      .length,
    low: analysisData.recommendations.filter((r) => r.priority === "low")
      .length,
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />

      <div className="pt-32 pb-20 px-6">
        <div className="max-w-6xl mx-auto">
          {/* Back Button */}
          <Link
            href="/upload"
            className="inline-flex items-center text-sm text-gray-600 hover:text-gray-900 mb-8"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Upload Another File
          </Link>

          {/* Header */}
          <div className="mb-10">
            <h1 className="text-4xl font-bold mb-3">Analysis Complete</h1>
            <p className="text-lg text-gray-600">
              Found {analysisData.summary.total_problems} issues in your data
            </p>
          </div>

          {/* Summary Cards */}
          <div className="grid md:grid-cols-4 gap-6 mb-10">
            <Card className="p-6 border-2">
              <FileSpreadsheet className="w-8 h-8 text-gray-400 mb-3" />
              <div className="text-3xl font-bold mb-1">
                {analysisData.file_info.rows}
              </div>
              <div className="text-sm text-gray-600">Total Rows</div>
            </Card>

            <Card className="p-6 border-2">
              <AlertCircle className="w-8 h-8 text-amber-500 mb-3" />
              <div className="text-3xl font-bold mb-1">
                {analysisData.summary.total_problems}
              </div>
              <div className="text-sm text-gray-600">Problems Found</div>
            </Card>

            <Card className="p-6 border-2">
              <CheckCircle2 className="w-8 h-8 text-emerald-600 mb-3" />
              <div className="text-3xl font-bold mb-1">
                {analysisData.summary.recommended_operations}
              </div>
              <div className="text-sm text-gray-600">Fixes Ready</div>
            </Card>

            <Card className="p-6 border-2 bg-emerald-50 border-emerald-200">
              <TrendingDown className="w-8 h-8 text-emerald-600 mb-3" />
              <div className="text-3xl font-bold mb-1 text-emerald-700">
                {Math.round(
                  (analysisData.summary.total_problems /
                    analysisData.file_info.rows) *
                    100,
                )}
                %
              </div>
              <div className="text-sm text-emerald-700 font-medium">
                Issues Detected
              </div>
            </Card>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            {/* Problems List */}
            <div className="md:col-span-2 space-y-6">
              <Card className="p-6 border-2">
                <h2 className="text-xl font-semibold mb-4">
                  Problems Detected
                </h2>

                {analysisData.problems_detected.length === 0 ? (
                  <div className="text-center py-8 text-gray-500">
                    <CheckCircle2 className="w-12 h-12 mx-auto mb-3 text-emerald-600" />
                    <p>No major issues detected!</p>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {analysisData.problems_detected
                      .slice(0, 10)
                      .map((problem, i) => (
                        <div
                          key={i}
                          className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                        >
                          <div className="flex-1">
                            <div className="font-medium text-sm">
                              {problem.column}
                            </div>
                            <div className="text-xs text-gray-600 capitalize">
                              {problem.problem_type.replace(/_/g, " ")}
                            </div>
                          </div>
                          <div className="flex items-center gap-3">
                            <Progress
                              value={problem.probability * 100}
                              className="w-20 h-2"
                            />
                            <span className="text-sm font-medium text-gray-700">
                              {Math.round(problem.probability * 100)}%
                            </span>
                          </div>
                        </div>
                      ))}
                  </div>
                )}
              </Card>

              {/* Recommendations */}
              <Card className="p-6 border-2">
                <h2 className="text-xl font-semibold mb-4">
                  Recommended Fixes
                </h2>

                <div className="space-y-3">
                  {analysisData.recommendations.slice(0, 8).map((rec, i) => (
                    <div
                      key={i}
                      className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg"
                    >
                      <Badge
                        variant={
                          rec.priority === "high" ? "destructive" : "secondary"
                        }
                        className="mt-0.5"
                      >
                        {rec.priority}
                      </Badge>
                      <div className="flex-1">
                        <div className="font-medium text-sm capitalize">
                          {rec.operation.replace(/_/g, " ")}
                          {rec.column && (
                            <span className="text-gray-600">
                              {" "}
                              → {rec.column}
                            </span>
                          )}
                        </div>
                        <div className="text-xs text-gray-600 mt-1">
                          {rec.reason}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </Card>
            </div>

            {/* Actions Sidebar */}
            <div className="space-y-6">
              <Card className="p-6 border-2 border-emerald-200 bg-emerald-50">
                <h3 className="font-semibold mb-4">Download Cleaned File</h3>
                <p className="text-sm text-gray-700 mb-6">
                  All {analysisData.summary.recommended_operations} fixes will
                  be applied automatically.
                </p>
                <Button
                  className="w-full mb-3"
                  onClick={handleDownloadClean}
                  disabled={downloading}
                >
                  {downloading ? "Processing..." : "Download Clean File"}
                  {!downloading && <Download className="ml-2 w-4 h-4" />}
                </Button>
                <p className="text-xs text-gray-600 text-center">
                  Format: CSV • Original preserved
                </p>
              </Card>

              <Card className="p-6 border-2">
                <h3 className="font-semibold mb-4">File Information</h3>
                <div className="space-y-3 text-sm">
                  <div>
                    <div className="text-gray-600">Filename</div>
                    <div className="font-medium truncate">
                      {analysisData.filename}
                    </div>
                  </div>
                  <div>
                    <div className="text-gray-600">Rows</div>
                    <div className="font-medium">
                      {analysisData.file_info.rows.toLocaleString()}
                    </div>
                  </div>
                  <div>
                    <div className="text-gray-600">Columns</div>
                    <div className="font-medium">
                      {analysisData.file_info.columns}
                    </div>
                  </div>
                </div>
              </Card>

              <Card className="p-6 border-2">
                <h3 className="font-semibold mb-4">Priority Breakdown</h3>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">High Priority</span>
                    <Badge variant="destructive">
                      {problemsByPriority.high}
                    </Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">
                      Medium Priority
                    </span>
                    <Badge variant="secondary">
                      {problemsByPriority.medium}
                    </Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Low Priority</span>
                    <Badge variant="outline">{problemsByPriority.low}</Badge>
                  </div>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
