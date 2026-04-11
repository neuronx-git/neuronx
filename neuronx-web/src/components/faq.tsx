"use client";

import { useState } from "react";
import { ChevronDown } from "lucide-react";

const faqs = [
  {
    q: "Does NeuronX replace our CRM?",
    a: "No. NeuronX works on top of GoHighLevel (GHL), which serves as your CRM. NeuronX is the intelligence layer — it handles AI calling, scoring, briefings, and analytics. GHL handles contacts, pipelines, email/SMS, and workflows.",
  },
  {
    q: "Is the AI compliant with RCIC regulations?",
    a: "Yes. NeuronX enforces strict trust boundaries. The AI never assesses immigration eligibility, recommends pathways, interprets law, or promises outcomes. It only collects information, asks factual questions, and books consultations. Every interaction is auditable.",
  },
  {
    q: "How long does onboarding take?",
    a: "2-4 hours. We install a pre-configured snapshot into your GHL account, customize branding, configure your RCIC team, and run a live test. Your firm is operational the same day.",
  },
  {
    q: "What if a prospect asks for legal advice during the AI call?",
    a: "The AI immediately escalates. If a prospect asks about eligibility, mentions deportation, or shows emotional distress, the call is flagged for human follow-up. Your team gets an instant alert.",
  },
  {
    q: "Can I see analytics on my pipeline?",
    a: "Yes. NeuronX includes Metabase-powered dashboards showing conversion rates, pipeline velocity, stuck leads, RCIC workload, and revenue per lead source. Metrics that GHL alone cannot provide.",
  },
  {
    q: "Do you support French-language intake?",
    a: "Multi-language support is on our roadmap for v2. Currently, NeuronX operates in English. The VAPI voice AI supports multiple accents and is trained to understand non-native English speakers.",
  },
  {
    q: "What immigration programs are supported?",
    a: "All major Canadian programs: Express Entry, Spousal Sponsorship, Work Permit, Study Permit, LMIA, PR Renewal, Citizenship, and Visitor Visa. Each has program-specific intake questions and nurture content.",
  },
];

export function FAQ() {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  return (
    <section id="faq" className="py-24 px-6 bg-[#FFFBF5]">
      <div className="max-w-3xl mx-auto">
        <h2 className="text-3xl md:text-4xl font-bold text-[#0F172A] tracking-tight text-center mb-16">
          Frequently asked questions
        </h2>

        <div className="space-y-3">
          {faqs.map((faq, i) => (
            <div
              key={i}
              className="border border-black/5 rounded-xl bg-white overflow-hidden"
            >
              <button
                onClick={() => setOpenIndex(openIndex === i ? null : i)}
                className="w-full flex items-center justify-between p-5 text-left"
              >
                <span className="font-medium text-[#0F172A] pr-4">
                  {faq.q}
                </span>
                <ChevronDown
                  size={18}
                  className={`text-slate-400 flex-shrink-0 transition-transform duration-200 ${
                    openIndex === i ? "rotate-180" : ""
                  }`}
                />
              </button>
              {openIndex === i && (
                <div className="px-5 pb-5 text-slate-500 text-sm leading-relaxed border-t border-black/5 pt-4">
                  {faq.a}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
