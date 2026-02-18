"use client";

import { Card } from "@/components/ui/card";
import {
  Database,
  Zap,
  Shield,
  FileSpreadsheet,
  TrendingUp,
  Check,
} from "lucide-react";
import { motion } from "framer-motion";

const features = [
  {
    icon: Database,
    title: "Smart Duplicate Detection",
    description:
      "ML-powered fuzzy matching finds exact and similar duplicates. Handles typos and case variations.",
  },
  {
    icon: Zap,
    title: "Intelligent Missing Values",
    description:
      "Statistical imputation using mean, median, or mode based on data distribution patterns.",
  },
  {
    icon: Shield,
    title: "Outlier Removal",
    description:
      "IQR and Z-score methods detect anomalies and typos automatically with 97% accuracy.",
  },
  {
    icon: FileSpreadsheet,
    title: "Format Standardization",
    description:
      "Consistent formatting for dates, phone numbers, and text casing across all rows.",
  },
  {
    icon: TrendingUp,
    title: "Instant Analysis",
    description:
      "XGBoost models analyze 5,000 rows in under 30 seconds with confidence scores.",
  },
  {
    icon: Check,
    title: "One-Click Cleaning",
    description:
      "Apply all recommended fixes instantly with full audit trail of changes made.",
  },
];

export function Features() {
  return (
    <section id="features" className="py-20 px-6 bg-gray-50">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold mb-4">
            Production-grade data cleaning
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Enterprise ML models. No code required. Export to CSV or Excel.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          {features.map((feature, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: i * 0.1 }}
              viewport={{ once: true }}
            >
              <Card className="p-6 h-full hover:shadow-lg transition-shadow border-gray-200">
                <div className="w-12 h-12 bg-emerald-50 rounded-lg flex items-center justify-center mb-4">
                  <feature.icon className="w-6 h-6 text-emerald-600" />
                </div>
                <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
                <p className="text-gray-600 text-sm leading-relaxed">
                  {feature.description}
                </p>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
