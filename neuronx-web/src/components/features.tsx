"use client";

import { motion } from "framer-motion";
import {
  Phone,
  BarChart3,
  FileText,
  Shield,
  Calendar,
  Bell,
  Users,
  Zap,
} from "lucide-react";

const features = [
  {
    icon: Phone,
    title: "AI Voice Intake",
    description:
      "Every inquiry gets an AI-powered follow-up call within 5 minutes. Structured R1-R5 readiness assessment with RCIC-safe compliance guardrails.",
    color: "bg-red-50 text-[#E8380D]",
  },
  {
    icon: BarChart3,
    title: "Lead Readiness Scoring",
    description:
      "Automatic 0-100 scoring across 5 dimensions: program interest, location, urgency, prior applications, and budget awareness.",
    color: "bg-amber-50 text-[#D9A651]",
  },
  {
    icon: FileText,
    title: "Consultation Briefings",
    description:
      "AI-assembled prep documents delivered to your RCIC before every meeting. Full prospect context, immigration history, and key questions.",
    color: "bg-blue-50 text-blue-600",
  },
  {
    icon: Calendar,
    title: "Smart Booking",
    description:
      "Qualified leads are automatically invited to book consultations. Reminders, no-show recovery, and rescheduling — all automated.",
    color: "bg-emerald-50 text-emerald-600",
  },
  {
    icon: Bell,
    title: "Pipeline Automation",
    description:
      "24 workflows manage the entire inquiry-to-retainer lifecycle. 7-step contact sequences, nurture programs, and stuck-lead detection.",
    color: "bg-purple-50 text-purple-600",
  },
  {
    icon: Shield,
    title: "Compliance Built In",
    description:
      "Trust boundaries enforced in every AI interaction. The AI never assesses eligibility, recommends pathways, or interprets law.",
    color: "bg-slate-50 text-slate-600",
  },
  {
    icon: Users,
    title: "Multi-Firm Ready",
    description:
      "One-click onboarding via GHL Snapshot. Each firm gets their own branded pipeline, workflows, and AI configuration.",
    color: "bg-orange-50 text-orange-600",
  },
  {
    icon: Zap,
    title: "Immigration-Specific",
    description:
      "Built for Canadian immigration from day one. IRCC-aligned programs, Express Entry, Spousal, Work Permit, Study, and more.",
    color: "bg-cyan-50 text-cyan-600",
  },
];

export function Features() {
  return (
    <section id="features" className="py-24 px-6 bg-white">
      <div className="max-w-6xl mx-auto">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-[#0F172A] tracking-tight">
            Everything your firm needs to
            <span className="text-[#E8380D]"> convert more clients</span>
          </h2>
          <p className="mt-4 text-lg text-slate-500">
            NeuronX handles the entire pre-retention funnel — from first inquiry
            to signed retainer — so your team focuses on consultations, not
            chasing leads.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, i) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-50px" }}
              transition={{ duration: 0.5, delay: i * 0.05 }}
              className="group p-6 rounded-2xl border border-black/5 bg-[#FFFBF5] hover:border-[#E8380D]/20 hover:shadow-lg hover:shadow-[#E8380D]/5 transition-all duration-300"
            >
              <div
                className={`w-10 h-10 rounded-xl ${feature.color} flex items-center justify-center mb-4`}
              >
                <feature.icon size={20} />
              </div>
              <h3 className="font-semibold text-[#0F172A] mb-2">
                {feature.title}
              </h3>
              <p className="text-sm text-slate-500 leading-relaxed">
                {feature.description}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
