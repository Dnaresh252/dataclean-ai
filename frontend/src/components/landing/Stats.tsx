"use client";

import { Clock, Target, FileSpreadsheet, TrendingUp } from "lucide-react";
import { motion } from "framer-motion";

const stats = [
  { value: "10+ hrs", label: "Saved weekly", icon: Clock },
  { value: "97%", label: "ML Accuracy", icon: Target },
  { value: "10K+", label: "Files cleaned", icon: FileSpreadsheet },
  { value: "500+", label: "Happy users", icon: TrendingUp },
];

export function Stats() {
  return (
    <section className="pb-20 px-6">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto"
        >
          {stats.map((stat, i) => (
            <div key={i} className="text-center">
              <stat.icon className="w-6 h-6 mx-auto mb-3 text-emerald-600" />
              <div className="text-3xl font-bold mb-1">{stat.value}</div>
              <div className="text-sm text-gray-600">{stat.label}</div>
            </div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}
