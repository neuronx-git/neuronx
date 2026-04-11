"use client";

import { useState } from "react";
import Link from "next/link";
import { Menu, X } from "lucide-react";

const navLinks = [
  { label: "Features", href: "#features" },
  { label: "How It Works", href: "#how-it-works" },
  { label: "Pricing", href: "#pricing" },
  { label: "FAQ", href: "#faq" },
];

export function Navbar() {
  const [open, setOpen] = useState(false);

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-[#FFFBF5]/80 backdrop-blur-lg border-b border-black/5">
      <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-[#0F172A] flex items-center justify-center">
            <span className="text-[#E8380D] font-bold text-xs">NX</span>
          </div>
          <span className="font-semibold text-lg text-[#0F172A]">NeuronX</span>
        </Link>

        {/* Desktop nav */}
        <nav className="hidden md:flex items-center gap-8">
          {navLinks.map((link) => (
            <a
              key={link.href}
              href={link.href}
              className="text-sm text-slate-600 hover:text-[#0F172A] transition-colors"
            >
              {link.label}
            </a>
          ))}
        </nav>

        {/* CTA buttons */}
        <div className="hidden md:flex items-center gap-3">
          <a
            href="#pricing"
            className="text-sm font-medium text-slate-600 hover:text-[#0F172A] transition-colors"
          >
            Log in
          </a>
          <a
            href="#cta"
            className="inline-flex items-center px-5 py-2.5 rounded-full bg-[#E8380D] text-white text-sm font-medium hover:bg-[#D42E06] transition-all hover:shadow-lg hover:shadow-[#E8380D]/20 hover:-translate-y-0.5"
          >
            Book a Demo
          </a>
        </div>

        {/* Mobile menu button */}
        <button
          className="md:hidden p-2"
          onClick={() => setOpen(!open)}
          aria-label="Toggle menu"
        >
          {open ? <X size={20} /> : <Menu size={20} />}
        </button>
      </div>

      {/* Mobile menu */}
      {open && (
        <div className="md:hidden bg-white border-t border-black/5 px-6 py-4 space-y-3">
          {navLinks.map((link) => (
            <a
              key={link.href}
              href={link.href}
              className="block text-sm text-slate-600 py-2"
              onClick={() => setOpen(false)}
            >
              {link.label}
            </a>
          ))}
          <a
            href="#cta"
            className="block w-full text-center px-5 py-2.5 rounded-full bg-[#E8380D] text-white text-sm font-medium"
            onClick={() => setOpen(false)}
          >
            Book a Demo
          </a>
        </div>
      )}
    </header>
  );
}
