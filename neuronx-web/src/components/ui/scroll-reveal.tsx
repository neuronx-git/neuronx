import { motion, useInView, useMotionValue, animate } from "framer-motion";
import { type ReactNode, useRef, useEffect, useState } from "react";

/* Premium easing — matches Stripe/Linear feel */
const premiumEase = [0.22, 1, 0.36, 1] as const;

/* ─── Scroll Reveal ─── */
interface ScrollRevealProps {
  children: ReactNode;
  className?: string;
  delay?: number;
  duration?: number;
  y?: number;
  once?: boolean;
}

export function ScrollReveal({
  children,
  className = "",
  delay = 0,
  duration = 0.6,
  y = 20,
  once = true,
}: ScrollRevealProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once, margin: "-60px" }}
      transition={{ duration, delay, ease: premiumEase }}
      className={className}
    >
      {children}
    </motion.div>
  );
}

/* ─── Stagger Container ─── */
interface StaggerProps {
  children: ReactNode;
  className?: string;
  staggerDelay?: number;
  once?: boolean;
}

export function StaggerContainer({
  children,
  className = "",
  staggerDelay = 0.08,
  once = true,
}: StaggerProps) {
  return (
    <motion.div
      initial="hidden"
      whileInView="visible"
      viewport={{ once, margin: "-60px" }}
      variants={{
        hidden: {},
        visible: { transition: { staggerChildren: staggerDelay } },
      }}
      className={className}
    >
      {children}
    </motion.div>
  );
}

export function StaggerItem({
  children,
  className = "",
}: {
  children: ReactNode;
  className?: string;
}) {
  return (
    <motion.div
      variants={{
        hidden: { opacity: 0, y: 16 },
        visible: {
          opacity: 1,
          y: 0,
          transition: { duration: 0.5, ease: premiumEase },
        },
      }}
      className={className}
    >
      {children}
    </motion.div>
  );
}

/* ─── Animated Counter ─── */
interface CounterProps {
  value: number;
  className?: string;
  suffix?: string;
  duration?: number;
}

export function AnimatedCounter({
  value,
  className = "",
  suffix = "",
  duration = 1.5,
}: CounterProps) {
  const ref = useRef<HTMLSpanElement>(null);
  const isInView = useInView(ref, { once: true, margin: "-100px" });
  const [displayValue, setDisplayValue] = useState(0);

  useEffect(() => {
    if (!isInView) return;
    const motionVal = useMotionValue(0);
    const unsubscribe = motionVal.on("change", (v) => setDisplayValue(Math.round(v)));
    animate(motionVal, value, { duration, ease: premiumEase });
    return unsubscribe;
  }, [isInView, value, duration]);

  return (
    <span ref={ref} className={className}>
      {displayValue}{suffix}
    </span>
  );
}

/* ─── Animated Bar ─── */
interface BarProps {
  value: number;
  delay?: number;
  className?: string;
}

export function AnimatedBar({ value, delay = 0, className = "" }: BarProps) {
  return (
    <motion.div
      initial={{ width: "0%" }}
      whileInView={{ width: `${value}%` }}
      viewport={{ once: true, margin: "-100px" }}
      transition={{ duration: 1.2, delay, ease: premiumEase }}
      className={className}
    />
  );
}

/* ─── Card Hover ─── */
export function HoverCard({
  children,
  className = "",
}: {
  children: ReactNode;
  className?: string;
}) {
  return (
    <motion.div
      whileHover={{
        y: -4,
        transition: { duration: 0.3, ease: premiumEase },
      }}
      className={className}
    >
      {children}
    </motion.div>
  );
}

/* ─── Slide In (for briefing panel) ─── */
export function SlideIn({
  children,
  className = "",
  direction = "right",
  delay = 0,
}: {
  children: ReactNode;
  className?: string;
  direction?: "left" | "right" | "up" | "down";
  delay?: number;
}) {
  const offsets = {
    left: { x: -30, y: 0 },
    right: { x: 30, y: 0 },
    up: { x: 0, y: -20 },
    down: { x: 0, y: 20 },
  };

  return (
    <motion.div
      initial={{ opacity: 0, ...offsets[direction] }}
      whileInView={{ opacity: 1, x: 0, y: 0 }}
      viewport={{ once: true, margin: "-60px" }}
      transition={{ duration: 0.6, delay, ease: premiumEase }}
      className={className}
    >
      {children}
    </motion.div>
  );
}
