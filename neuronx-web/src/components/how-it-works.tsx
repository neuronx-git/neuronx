"use client";

import { motion } from "framer-motion";

const steps = [
  {
    number: "01",
    title: "Prospect Submits Inquiry",
    description:
      "A potential client fills out your branded intake form — online, from an ad, or from your website. Their information flows into your pipeline instantly.",
    accent: "#E8380D",
  },
  {
    number: "02",
    title: "AI Calls Within 5 Minutes",
    description:
      "NeuronX's AI calls the prospect, asks structured readiness questions (program, urgency, location, budget), and scores them 0-100. All compliant — no eligibility advice.",
    accent: "#D9A651",
  },
  {
    number: "03",
    title: "Qualified Leads Book Automatically",
    description:
      "High-scoring leads receive a booking link instantly. Low-scoring leads enter a nurture sequence. No lead falls through the cracks.",
    accent: "#10B981",
  },
  {
    number: "04",
    title: "RCIC Gets a Full Briefing",
    description:
      "Before every consultation, your RCIC receives an AI-prepared briefing: prospect profile, immigration goals, key questions, and recommended talking points.",
    accent: "#3B82F6",
  },
  {
    number: "05",
    title: "Client Signs Retainer",
    description:
      "After a prepared, professional consultation, the prospect signs. NeuronX tracks the entire funnel — conversion rates, bottlenecks, and revenue per lead.",
    accent: "#8B5CF6",
  },
];

export function HowItWorks() {
  return (
    <section id="how-it-works" className="py-24 px-6 bg-[#FFFBF5]">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-[#0F172A] tracking-tight">
            From inquiry to retainer in
            <span className="text-[#E8380D]"> 5 automated steps</span>
          </h2>
          <p className="mt-4 text-lg text-slate-500">
            NeuronX manages the complete pre-retention lifecycle. Your team
            focuses on delivering great consultations.
          </p>
        </div>

        <div className="space-y-8">
          {steps.map((step, i) => (
            <motion.div
              key={step.number}
              initial={{ opacity: 0, x: -30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true, margin: "-50px" }}
              transition={{ duration: 0.5, delay: i * 0.1 }}
              className="flex gap-6 items-start"
            >
              <div
                className="flex-shrink-0 w-12 h-12 rounded-2xl flex items-center justify-center text-white font-bold text-sm"
                style={{ backgroundColor: step.accent }}
              >
                {step.number}
              </div>
              <div>
                <h3 className="text-lg font-semibold text-[#0F172A] mb-1">
                  {step.title}
                </h3>
                <p className="text-slate-500 leading-relaxed">
                  {step.description}
                </p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
