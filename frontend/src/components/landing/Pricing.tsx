import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Check } from "lucide-react";
import Link from "next/link";

const plans = [
  {
    name: "Free",
    price: "₹0",
    period: "/month",
    features: [
      "2 files per month",
      "Up to 1,000 rows",
      "Basic cleaning",
      "Email support (48h)",
    ],
    cta: "Start Free",
    href: "/upload",
    popular: false,
  },
  {
    name: "Pro",
    price: "₹499",
    period: "/month",
    features: [
      "50 files per month",
      "Up to 10,000 rows",
      "ML-powered cleaning",
      "Priority support (4h)",
      "API access",
      "Batch processing",
    ],
    cta: "Upgrade to Pro",
    href: "#",
    popular: true,
  },
];

export function Pricing() {
  return (
    <section id="pricing" className="py-20 px-6 bg-gray-50">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold mb-4">
            Simple, transparent pricing
          </h2>
          <p className="text-lg text-gray-600">
            Start free. Scale as you grow.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          {plans.map((plan, i) => (
            <Card
              key={i}
              className={`p-8 relative ${
                plan.popular
                  ? "border-2 border-emerald-600 shadow-lg"
                  : "border-2"
              }`}
            >
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 -translate-x-1/2">
                  <span className="bg-emerald-600 text-white px-4 py-1 rounded-full text-sm font-medium">
                    Most Popular
                  </span>
                </div>
              )}

              <div className="mb-6">
                <h3 className="text-2xl font-bold mb-2">{plan.name}</h3>
                <div className="flex items-baseline gap-1">
                  <span className="text-5xl font-bold">{plan.price}</span>
                  <span className="text-gray-600">{plan.period}</span>
                </div>
              </div>

              <ul className="space-y-3 mb-8">
                {plan.features.map((feature, j) => (
                  <li key={j} className="flex items-start gap-3">
                    <Check className="w-5 h-5 text-emerald-600 flex-shrink-0 mt-0.5" />
                    <span className="text-gray-700">{feature}</span>
                  </li>
                ))}
              </ul>

              <Link href={plan.href}>
                <Button
                  className={`w-full ${plan.popular ? "" : "variant-outline"}`}
                  variant={plan.popular ? "default" : "outline"}
                >
                  {plan.cta}
                </Button>
              </Link>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
