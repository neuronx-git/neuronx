"use client";

import { motion } from "framer-motion";
import { Check } from "lucide-react";

const plans = [
  {
    name: "Essentials",
    price: "$299",
    period: "/month",
    currency: "CAD",
    description: "For firms starting with AI-powered intake",
    features: [
      "AI voice intake (up to 100 calls/mo)",
      "Lead readiness scoring (R1-R5)",
      "1 pipeline with 10 stages",
      "Automated booking + reminders",
      "No-show recovery workflow",
      "Email + SMS sequences",
      "Basic pipeline analytics",
    ],
    cta: "Start Free Trial",
    popular: false,
    accent: "border-slate-200",
  },
  {
    name: "Professional",
    price: "$599",
    period: "/month",
    currency: "CAD",
    description: "For growing firms that want full automation",
    features: [
      "Everything in Essentials",
      "Unlimited AI calls",
      "Pre-consultation briefings",
      "9-branch program nurture",
      "IRCC form data sheets",
      "Chrome extension (IRCC auto-fill)",
      "Advanced analytics (Metabase)",
      "Case processing pipeline",
      "Priority support",
    ],
    cta: "Start Free Trial",
    popular: true,
    accent: "border-[#E8380D]",
  },
  {
    name: "Scale",
    price: "$1,199",
    period: "/month",
    currency: "CAD",
    description: "For multi-RCIC firms and high-volume practices",
    features: [
      "Everything in Professional",
      "Multi-RCIC round-robin",
      "E-signatures (Documenso)",
      "Custom client portal",
      "Commission tracking",
      "Dedicated success manager",
      "Custom integrations",
      "SLA guarantee",
    ],
    cta: "Contact Sales",
    popular: false,
    accent: "border-slate-200",
  },
];

export function Pricing() {
  return (
    <section id="pricing" className="py-24 px-6 bg-white">
      <div className="max-w-6xl mx-auto">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-[#0F172A] tracking-tight">
            Simple, per-firm pricing.
            <span className="text-[#E8380D]"> No per-seat fees.</span>
          </h2>
          <p className="mt-4 text-lg text-slate-500">
            One retained client pays for months of NeuronX. All plans include
            14-day free trial — no credit card required.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          {plans.map((plan, i) => (
            <motion.div
              key={plan.name}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: i * 0.1 }}
              className={`relative rounded-2xl border-2 ${plan.accent} bg-white p-8 ${
                plan.popular ? "shadow-xl shadow-[#E8380D]/10 scale-105" : ""
              }`}
            >
              {plan.popular && (
                <div className="absolute -top-3 left-1/2 -translate-x-1/2 px-4 py-1 rounded-full bg-[#E8380D] text-white text-xs font-semibold">
                  Most Popular
                </div>
              )}

              <div className="mb-6">
                <h3 className="text-lg font-semibold text-[#0F172A]">
                  {plan.name}
                </h3>
                <p className="text-sm text-slate-500 mt-1">{plan.description}</p>
              </div>

              <div className="mb-6">
                <span className="text-4xl font-bold text-[#0F172A]">
                  {plan.price}
                </span>
                <span className="text-slate-500">{plan.period}</span>
                <span className="text-xs text-slate-400 ml-1">
                  {plan.currency}
                </span>
              </div>

              <ul className="space-y-3 mb-8">
                {plan.features.map((feature) => (
                  <li key={feature} className="flex items-start gap-2 text-sm">
                    <Check
                      size={16}
                      className="text-emerald-500 flex-shrink-0 mt-0.5"
                    />
                    <span className="text-slate-600">{feature}</span>
                  </li>
                ))}
              </ul>

              <a
                href="#cta"
                className={`block w-full text-center py-3 rounded-full font-medium text-sm transition-all ${
                  plan.popular
                    ? "bg-[#E8380D] text-white hover:bg-[#D42E06] hover:shadow-lg"
                    : "bg-[#0F172A] text-white hover:bg-[#1E293B]"
                }`}
              >
                {plan.cta}
              </a>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
