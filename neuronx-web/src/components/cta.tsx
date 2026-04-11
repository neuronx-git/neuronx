"use client";

import { motion } from "framer-motion";
import { ArrowRight } from "lucide-react";

export function CTA() {
  return (
    <section id="cta" className="relative py-24 px-6 bg-[#0F172A] overflow-hidden">
      {/* Decorative elements */}
      <div className="absolute top-0 right-0 w-80 h-80 bg-[#E8380D]/10 rounded-full blur-3xl" />
      <div className="absolute bottom-0 left-1/4 w-60 h-60 bg-[#D9A651]/10 rounded-full blur-3xl" />

      <motion.div
        initial={{ opacity: 0, y: 30 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6 }}
        className="max-w-3xl mx-auto text-center relative"
      >
        <h2 className="text-3xl md:text-5xl font-bold text-white tracking-tight leading-tight">
          Stop losing clients to
          <span className="text-[#E8380D]"> slow follow-up</span>
        </h2>
        <p className="mt-6 text-lg text-slate-300 max-w-xl mx-auto">
          Every hour you wait to respond, your competitor gets closer. NeuronX
          ensures every inquiry gets a professional response in under 5 minutes.
        </p>

        <div className="mt-10 flex flex-col sm:flex-row gap-4 justify-center">
          <a
            href="https://api.leadconnectorhq.com/widget/booking/clvODWkfByOZnzeqyPPW"
            className="inline-flex items-center justify-center gap-2 px-8 py-4 rounded-full bg-[#E8380D] text-white font-semibold text-base hover:bg-[#D42E06] transition-all hover:shadow-xl hover:shadow-[#E8380D]/30 hover:-translate-y-0.5"
          >
            Book a 30-Minute Demo
            <ArrowRight size={18} />
          </a>
        </div>

        <p className="mt-6 text-sm text-slate-400">
          14-day free trial. No credit card required. Cancel anytime.
        </p>
      </motion.div>
    </section>
  );
}
