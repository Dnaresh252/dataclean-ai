import { Navigation } from "@/components/shared/Navigation";
import { Hero } from "@/components/landing/Hero";
import { Stats } from "@/components/landing/Stats";
import { Features } from "@/components/landing/Features";
import { Pricing } from "@/components/landing/Pricing";
import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";
import Link from "next/link";

export default function LandingPage() {
  return (
    <main>
      <Navigation />
      <Hero />
      <Stats />
      <Features />

      {/* How It Works Section */}
      <section className="py-20 px-6">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">
              Three steps to clean data
            </h2>
            <p className="text-lg text-gray-600">
              Upload. Analyze. Download. That simple.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-12">
            {[
              {
                step: "01",
                title: "Upload file",
                description:
                  "Drag and drop CSV or Excel. Files up to 10,000 rows supported.",
              },
              {
                step: "02",
                title: "Review analysis",
                description:
                  "ML models show detected problems with confidence scores and recommendations.",
              },
              {
                step: "03",
                title: "Download clean data",
                description:
                  "Get cleaned file instantly. Plus detailed report of all changes made.",
              },
            ].map((step, i) => (
              <div key={i} className="text-center">
                <div className="text-6xl font-bold text-emerald-100 mb-4">
                  {step.step}
                </div>
                <h3 className="text-xl font-semibold mb-3">{step.title}</h3>
                <p className="text-gray-600 leading-relaxed">
                  {step.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <Pricing />

      {/* Social Proof Section */}
      <section className="py-20 px-6 bg-gray-50">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">
              Trusted by data professionals
            </h2>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                quote:
                  "Saves me 2 hours every day. The duplicate detection is incredibly accurate.",
                author: "Priya Sharma",
                role: "Data Analyst, Tech Startup",
              },
              {
                quote:
                  "Finally, a tool that actually understands messy data. XGBoost models are brilliant.",
                author: "Rahul Verma",
                role: "Senior Analyst, E-commerce",
              },
              {
                quote:
                  "We process 100+ vendor files monthly. DataClean reduced our cleaning time by 80%.",
                author: "Sneha Patel",
                role: "Operations Manager, FMCG",
              },
            ].map((testimonial, i) => (
              <div key={i} className="bg-white p-6 rounded-lg border">
                <p className="text-gray-700 mb-4 italic">
                  "{testimonial.quote}"
                </p>
                <div>
                  <div className="font-semibold">{testimonial.author}</div>
                  <div className="text-sm text-gray-600">
                    {testimonial.role}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="py-24 px-6 bg-gradient-to-br from-emerald-600 to-teal-700 text-white">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            Stop wasting time on data cleaning
          </h2>
          <p className="text-xl text-emerald-50 mb-10 max-w-2xl mx-auto">
            Join 500+ analysts who save 10+ hours per week with ML-powered
            cleaning
          </p>
          <Link href="/signup">
            <Button
              size="lg"
              variant="secondary"
              className="h-14 px-10 text-lg bg-white text-gray-900 hover:bg-gray-100"
            >
              Start Cleaning Free
              <ArrowRight className="ml-2 w-5 h-5" />
            </Button>
          </Link>
          <p className="text-sm text-emerald-100 mt-6">
            No credit card · 2 free files monthly · Cancel anytime
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-6 border-t bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            <div>
              <div className="font-semibold mb-3">Product</div>
              <div className="space-y-2 text-sm text-gray-600">
                <div>
                  <Link href="#features" className="hover:text-gray-900">
                    Features
                  </Link>
                </div>
                <div>
                  <Link href="#pricing" className="hover:text-gray-900">
                    Pricing
                  </Link>
                </div>
                <div>
                  <Link href="/signup" className="hover:text-gray-900">
                    Try Free
                  </Link>
                </div>
              </div>
            </div>

            <div>
              <div className="font-semibold mb-3">Company</div>
              <div className="space-y-2 text-sm text-gray-600">
                <div>
                  <Link href="#" className="hover:text-gray-900">
                    About
                  </Link>
                </div>
                <div>
                  <Link href="#" className="hover:text-gray-900">
                    Blog
                  </Link>
                </div>
                <div>
                  <Link href="#" className="hover:text-gray-900">
                    Careers
                  </Link>
                </div>
              </div>
            </div>

            <div>
              <div className="font-semibold mb-3">Resources</div>
              <div className="space-y-2 text-sm text-gray-600">
                <div>
                  <Link href="#" className="hover:text-gray-900">
                    Documentation
                  </Link>
                </div>
                <div>
                  <Link href="#" className="hover:text-gray-900">
                    API Reference
                  </Link>
                </div>
                <div>
                  <Link href="#" className="hover:text-gray-900">
                    Support
                  </Link>
                </div>
              </div>
            </div>

            <div>
              <div className="font-semibold mb-3">Legal</div>
              <div className="space-y-2 text-sm text-gray-600">
                <div>
                  <Link href="#" className="hover:text-gray-900">
                    Privacy Policy
                  </Link>
                </div>
                <div>
                  <Link href="#" className="hover:text-gray-900">
                    Terms of Service
                  </Link>
                </div>
                <div>
                  <Link href="#" className="hover:text-gray-900">
                    GDPR
                  </Link>
                </div>
              </div>
            </div>
          </div>

          <div className="pt-8 border-t text-center text-sm text-gray-600">
            <p>
              © 2025 DataClean.AI · Built with Next.js 14 & XGBoost ML · Made in
              India 🇮🇳
            </p>
          </div>
        </div>
      </footer>
    </main>
  );
}
