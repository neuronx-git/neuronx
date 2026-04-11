import Link from "next/link";

export function Footer() {
  return (
    <footer className="bg-[#0F172A] border-t border-white/10 py-12 px-6">
      <div className="max-w-6xl mx-auto">
        <div className="grid md:grid-cols-4 gap-8 mb-12">
          {/* Brand */}
          <div>
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 rounded-lg bg-white/10 flex items-center justify-center">
                <span className="text-[#E8380D] font-bold text-xs">NX</span>
              </div>
              <span className="font-semibold text-white">NeuronX</span>
            </div>
            <p className="text-sm text-slate-400 leading-relaxed">
              AI-powered sales operating system for Canadian immigration
              consulting firms.
            </p>
          </div>

          {/* Product */}
          <div>
            <h4 className="text-sm font-semibold text-white mb-4">Product</h4>
            <ul className="space-y-2">
              {["Features", "Pricing", "How It Works", "FAQ"].map((item) => (
                <li key={item}>
                  <a
                    href={`#${item.toLowerCase().replace(/ /g, "-")}`}
                    className="text-sm text-slate-400 hover:text-white transition-colors"
                  >
                    {item}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Programs */}
          <div>
            <h4 className="text-sm font-semibold text-white mb-4">
              Programs
            </h4>
            <ul className="space-y-2">
              {[
                "Express Entry",
                "Spousal Sponsorship",
                "Work Permit",
                "Study Permit",
                "LMIA",
                "Citizenship",
              ].map((item) => (
                <li key={item}>
                  <span className="text-sm text-slate-400">{item}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Company */}
          <div>
            <h4 className="text-sm font-semibold text-white mb-4">Company</h4>
            <ul className="space-y-2">
              {[
                { label: "About", href: "#" },
                { label: "Blog", href: "#" },
                { label: "Contact", href: "mailto:hello@neuronx.co" },
                { label: "Privacy Policy", href: "#" },
              ].map((item) => (
                <li key={item.label}>
                  <a
                    href={item.href}
                    className="text-sm text-slate-400 hover:text-white transition-colors"
                  >
                    {item.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="border-t border-white/10 pt-8 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-sm text-slate-500">
            &copy; {new Date().getFullYear()} NeuronX. All rights reserved.
          </p>
          <p className="text-xs text-slate-600">
            NeuronX is not a law firm and does not provide immigration advice.
          </p>
        </div>
      </div>
    </footer>
  );
}
