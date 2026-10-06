'use client'
import { motion } from "motion/react"

export default function Spinner() {
  const bars = Array.from({ length: 12 });

  return (
    <div className="relative w-5 h-5">
      {bars.map((_, i) => {
        const rotation = i * 30; // 360 / 12 bars
        return (
          <motion.div
            key={i}
            className="absolute left-1/2 top-1/2 w-[2px] h-[5px] bg-white rounded-sm"
            style={{
              transform: `rotate(${rotation}deg) translate(0, -140%)`,
              transformOrigin: "center",
            }}
            animate={{ opacity: [1, 0.15] }}
            transition={{
              duration: 1,
              repeat: Infinity,
              ease: "linear",
              delay: -(1 - (i / 12)), // offsets each bar's phase in the loop
            }}
          />
        );
      })}
    </div>
  );
}