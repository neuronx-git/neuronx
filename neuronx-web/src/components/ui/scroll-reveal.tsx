import { motion, useInView } from "framer-motion";
import { type ReactNode, useRef, useState, useEffect } from "react";

/* Premium easing */
const ease = [0.22, 1, 0.36, 1] as const;

/* ─── Scroll Reveal ───
 * VISIBLE MOVEMENT: y:40px (was 20), duration 0.7s, triggers when 20% visible
 */
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
  duration = 0.7,
  y = 40,
  once = true,
}: ScrollRevealProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once, amount: 0.2 }}
      transition={{ duration, delay, ease }}
      className={className}
    >
      {children}
    </motion.div>
  );
}

/* ─── Stagger Container ───
 * VISIBLE STAGGER: 0.15s between children (was 0.08)
 */
interface StaggerProps {
  children: ReactNode;
  className?: string;
  staggerDelay?: number;
  once?: boolean;
}

export function StaggerContainer({
  children,
  className = "",
  staggerDelay = 0.15,
  once = true,
}: StaggerProps) {
  return (
    <motion.div
      initial="hidden"
      whileInView="visible"
      viewport={{ once, amount: 0.15 }}
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
        hidden: { opacity: 0, y: 30, scale: 0.95 },
        visible: {
          opacity: 1,
          y: 0,
          scale: 1,
          transition: { duration: 0.6, ease },
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
  duration = 2,
}: CounterProps) {
  const ref = useRef<HTMLSpanElement>(null);
  const isInView = useInView(ref, { once: true, amount: 0.5 });
  const [displayValue, setDisplayValue] = useState(0);

  useEffect(() => {
    if (!isInView) return;
    let start = 0;
    const step = value / (duration * 60); // 60fps
    const timer = setInterval(() => {
      start += step;
      if (start >= value) {
        setDisplayValue(value);
        clearInterval(timer);
      } else {
        setDisplayValue(Math.floor(start));
      }
    }, 1000 / 60);
    return () => clearInterval(timer);
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
      viewport={{ once: true, amount: 0.3 }}
      transition={{ duration: 1.2, delay, ease }}
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
        y: -6,
        scale: 1.02,
        transition: { duration: 0.3, ease },
      }}
      className={className}
    >
      {children}
    </motion.div>
  );
}

/* ─── Slide In ─── */
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
    left: { x: -40, y: 0 },
    right: { x: 40, y: 0 },
    up: { x: 0, y: -30 },
    down: { x: 0, y: 30 },
  };

  return (
    <motion.div
      initial={{ opacity: 0, ...offsets[direction] }}
      whileInView={{ opacity: 1, x: 0, y: 0 }}
      viewport={{ once: true, amount: 0.2 }}
      transition={{ duration: 0.7, delay, ease }}
      className={className}
    >
      {children}
    </motion.div>
  );
}
