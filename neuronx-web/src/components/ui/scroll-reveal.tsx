"use client";

import { motion, type Variants } from "framer-motion";
import { type ReactNode } from "react";

interface ScrollRevealProps {
  children: ReactNode;
  className?: string;
  delay?: number;
  duration?: number;
  y?: number;
  once?: boolean;
}

const revealVariants: Variants = {
  hidden: (custom: { y: number }) => ({
    opacity: 0,
    y: custom.y,
  }),
  visible: (custom: { duration: number; delay: number }) => ({
    opacity: 1,
    y: 0,
    transition: {
      duration: custom.duration,
      delay: custom.delay,
      ease: [0.25, 0.4, 0.25, 1],
    },
  }),
};

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
      initial="hidden"
      whileInView="visible"
      viewport={{ once, margin: "-50px" }}
      custom={{ y, duration, delay }}
      variants={revealVariants}
      className={className}
    >
      {children}
    </motion.div>
  );
}

// Stagger container for child elements
interface StaggerContainerProps {
  children: ReactNode;
  className?: string;
  staggerDelay?: number;
  once?: boolean;
}

const containerVariants: Variants = {
  hidden: {},
  visible: (custom: { staggerDelay: number }) => ({
    transition: {
      staggerChildren: custom.staggerDelay,
    },
  }),
};

const itemVariants: Variants = {
  hidden: { opacity: 0, y: 16 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, ease: [0.25, 0.4, 0.25, 1] },
  },
};

export function StaggerContainer({
  children,
  className = "",
  staggerDelay = 0.1,
  once = true,
}: StaggerContainerProps) {
  return (
    <motion.div
      initial="hidden"
      whileInView="visible"
      viewport={{ once, margin: "-50px" }}
      custom={{ staggerDelay }}
      variants={containerVariants}
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
    <motion.div variants={itemVariants} className={className}>
      {children}
    </motion.div>
  );
}

// Animated counter for numbers
interface CounterProps {
  value: number;
  className?: string;
  suffix?: string;
}

export function AnimatedCounter({ value, className = "", suffix = "" }: CounterProps) {
  return (
    <motion.span
      className={className}
      initial={{ opacity: 0 }}
      whileInView={{ opacity: 1 }}
      viewport={{ once: true }}
    >
      <motion.span
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        transition={{ duration: 0.5 }}
      >
        {value}{suffix}
      </motion.span>
    </motion.span>
  );
}
