"use client";

import { motion } from "framer-motion";
import { Phone, Clock, Brain, ArrowRight } from "lucide-react";

export function Hero() {
  return (
    <section className="relative pt-32 pb-20 px-6 overflow-hidden bg-[#0F172A]">
      {/* Decorative gradient shapes */}
      <div className="absolute top-0 right-0 w-96 h-96 bg-[#E8380D]/10 rounded-full blur-3xl" />
      <div className="absolute bottom-0 left-0 w-80 h-80 bg-[#D9A651]/10 rounded-full blur-3xl" />

      <div className="max-w-6xl mx-auto relative">
        <div className="max-w-3xl">
          {/* Badge */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 text-white/80 text-sm mb-8 border border-white/10"
          >
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            Built for Canadian RCIC firms
          </motion.div>

          {/* Headline */}
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="text-4xl md:text-6xl font-bold text-white leading-[1.1] tracking-tight"
          >
            Every inquiry
            <span className="text-[#E8380D]"> answered in 5 minutes.</span>
            <br />
            Every consultation
            <span className="text-[#D9A651]"> fully prepared.</span>
          </motion.h1>

          {/* Subheadline */}
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="mt-6 text-lg md:text-xl text-slate-300 max-w-2xl leading-relaxed"
          >
            NeuronX is the AI-powered sales operating system that turns immigration
            inquiries into retained clients. Automated intake calls, structured
            readiness scoring, and pre-consultation briefings — so your RCICs
            walk into every meeting prepared.
          </motion.p>

          {/* CTAs */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="mt-10 flex flex-col sm:flex-row gap-4"
          >
            <a
              href="#cta"
              className="inline-flex items-center justify-center gap-2 px-8 py-4 rounded-full bg-[#E8380D] text-white font-semibold text-base hover:bg-[#D42E06] transition-all hover:shadow-xl hover:shadow-[#E8380D]/30 hover:-translate-y-0.5"
            >
              Book a Demo
              <ArrowRight size={18} />
            </a>
            <a
              href="#how-it-works"
              className="inline-flex items-center justify-center gap-2 px-8 py-4 rounded-full border border-white/20 text-white font-medium text-base hover:bg-white/10 transition-all"
            >
              See How It Works
            </a>
          </motion.div>

          {/* Stats row */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="mt-16 grid grid-cols-3 gap-8 max-w-lg"
          >
            {[
              { icon: Clock, value: "< 5 min", label: "First contact" },
              { icon: Phone, value: "24/7", label: "AI intake calls" },
              { icon: Brain, value: "100%", label: "Briefings prepared" },
            ].map((stat) => (
              <div key={stat.label} className="text-center">
                <stat.icon size={20} className="text-[#D9A651] mx-auto mb-2" />
                <div className="text-2xl font-bold text-white">{stat.value}</div>
                <div className="text-xs text-slate-400 mt-1">{stat.label}</div>
              </div>
            ))}
          </motion.div>
        </div>
      </div>
    </section>
  );
}
