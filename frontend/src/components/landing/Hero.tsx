"use client";

import { Button } from "@/components/ui/button";
import { ArrowRight, Check, Sparkles, Zap, Database } from "lucide-react";
import Link from "next/link";
import { motion } from "framer-motion";

export function Hero() {
  return (
    <section className="relative pt-32 pb-20 px-6 overflow-hidden">
      {/* Animated Background Gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-emerald-50 via-white to-blue-50 opacity-60" />
      <div className="absolute inset-0">
        <div className="absolute top-20 left-10 w-72 h-72 bg-emerald-200 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob" />
        <div className="absolute top-40 right-10 w-72 h-72 bg-blue-200 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000" />
        <div className="absolute bottom-20 left-1/2 w-72 h-72 bg-purple-200 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-4000" />
      </div>

      <div className="max-w-7xl mx-auto relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center max-w-4xl mx-auto"
        >
          {/* Badge */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2 }}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-gradient-to-r from-emerald-50 to-blue-50 border border-emerald-200 mb-8 shadow-sm"
          >
            <Sparkles className="w-4 h-4 text-emerald-600" />
            <span className="text-sm font-semibold bg-gradient-to-r from-emerald-700 to-blue-700 bg-clip-text text-transparent">
              AI-Powered Data Cleaning
            </span>
            <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" />
          </motion.div>

          {/* Main Headline */}
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="text-5xl md:text-6xl lg:text-7xl font-bold mb-6 leading-tight"
          >
            Clean messy data in{" "}
            <span className="relative inline-block">
              <span className="bg-gradient-to-r from-emerald-600 via-teal-600 to-blue-600 bg-clip-text text-transparent">
                30 seconds
              </span>
              <motion.div
                className="absolute -bottom-2 left-0 right-0 h-3 bg-gradient-to-r from-emerald-200 to-blue-200 -z-10"
                initial={{ scaleX: 0 }}
                animate={{ scaleX: 1 }}
                transition={{ delay: 0.8, duration: 0.6 }}
              />
            </span>
          </motion.h1>

          {/* Subheadline */}
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
            className="text-xl text-gray-600 mb-10 max-w-2xl mx-auto leading-relaxed"
          >
            XGBoost ML models detect and fix duplicates, missing values, and
            outliers automatically.
            <span className="font-semibold text-gray-900">
              {" "}
              Save 10+ hours per week.
            </span>
          </motion.p>

          {/* CTA Buttons */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
            className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-10"
          >
            <Link href="/signup">
              <Button
                size="lg"
                className="h-14 px-8 text-lg bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 shadow-lg shadow-emerald-200 transition-all hover:shadow-xl hover:shadow-emerald-300"
              >
                <Zap className="mr-2 w-5 h-5" />
                Start Cleaning Free
                <ArrowRight className="ml-2 w-5 h-5" />
              </Button>
            </Link>
            <Button
              size="lg"
              variant="outline"
              className="h-14 px-8 text-lg border-2 hover:bg-gray-50"
            >
              <Database className="mr-2 w-5 h-5" />
              View Demo
            </Button>
          </motion.div>

          {/* Trust Indicators */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.7 }}
            className="flex flex-wrap items-center justify-center gap-6 text-sm text-gray-600"
          >
            <div className="flex items-center gap-2 px-4 py-2 bg-white rounded-full border shadow-sm">
              <Check className="w-4 h-4 text-emerald-600" />
              <span className="font-medium">No credit card</span>
            </div>
            <div className="flex items-center gap-2 px-4 py-2 bg-white rounded-full border shadow-sm">
              <Check className="w-4 h-4 text-emerald-600" />
              <span className="font-medium">2 files free monthly</span>
            </div>
            <div className="flex items-center gap-2 px-4 py-2 bg-white rounded-full border shadow-sm">
              <Check className="w-4 h-4 text-emerald-600" />
              <span className="font-medium">Auto-delete in 24h</span>
            </div>
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
}
