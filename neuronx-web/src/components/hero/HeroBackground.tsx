import { motion } from "framer-motion";

/**
 * 4-Layer Hero Background System
 * L1: Base color
 * L2: Radial glows (static)
 * L3: Animated gradient overlay (slow drift)
 * L4: Grain texture
 */
export const HeroBackground = () => {
  return (
    <div className="absolute inset-0 overflow-hidden">
      {/* Layer 1 — Base (handled by parent className) */}

      {/* Layer 2 — Radial glows */}
      <div
        className="absolute inset-0"
        style={{
          background: [
            "radial-gradient(ellipse 60% 50% at 15% 25%, rgba(79,70,229,0.22) 0%, transparent 70%)",
            "radial-gradient(ellipse 50% 40% at 85% 20%, rgba(124,58,237,0.18) 0%, transparent 70%)",
            "radial-gradient(ellipse 70% 50% at 50% 85%, rgba(59,130,246,0.12) 0%, transparent 70%)",
          ].join(", "),
        }}
      />

      {/* Layer 3 — Animated gradient (slow drift) */}
      <motion.div
        className="absolute inset-0 opacity-[0.07]"
        animate={{
          backgroundPosition: ["0% 0%", "100% 50%", "50% 100%", "0% 0%"],
        }}
        transition={{
          duration: 22,
          ease: "linear",
          repeat: Infinity,
        }}
        style={{
          backgroundSize: "400% 400%",
          backgroundImage:
            "linear-gradient(135deg, rgba(79,70,229,0.5), transparent 40%, rgba(124,58,237,0.4), transparent 60%, rgba(59,130,246,0.3))",
        }}
      />

      {/* Layer 4 — Grain texture */}
      <div
        className="absolute inset-0 opacity-[0.03] mix-blend-overlay pointer-events-none"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")`,
        }}
      />

      {/* Layer 5 — Subtle grid (optional) */}
      <div
        className="absolute inset-0 opacity-[0.025] pointer-events-none"
        style={{
          backgroundImage:
            "linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px)",
          backgroundSize: "70px 70px",
        }}
      />
    </div>
  );
};

/**
 * Light mode hero background — soft blue wash with depth
 */
export const HeroBackgroundLight = () => {
  return (
    <div className="absolute inset-0 overflow-hidden">
      <div
        className="absolute inset-0"
        style={{
          background: [
            "radial-gradient(ellipse 60% 50% at 20% 30%, rgba(79,70,229,0.06) 0%, transparent 70%)",
            "radial-gradient(ellipse 50% 40% at 80% 25%, rgba(124,58,237,0.04) 0%, transparent 70%)",
            "radial-gradient(ellipse 70% 50% at 50% 80%, rgba(59,130,246,0.03) 0%, transparent 70%)",
          ].join(", "),
        }}
      />
    </div>
  );
};
