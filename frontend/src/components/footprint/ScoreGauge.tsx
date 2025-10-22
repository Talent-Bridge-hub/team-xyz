import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';

interface ScoreGaugeProps {
  score: number;
  size?: number;
}

export default function ScoreGauge({ score, size = 200 }: ScoreGaugeProps) {
  const [animatedScore, setAnimatedScore] = useState(0);

  useEffect(() => {
    const timer = setTimeout(() => {
      setAnimatedScore(score);
    }, 100);
    return () => clearTimeout(timer);
  }, [score]);

  const radius = size / 2 - 20;
  const circumference = 2 * Math.PI * radius;
  const progress = (animatedScore / 100) * circumference;

  // Color based on score
  const getColor = () => {
    if (score >= 85) return { from: '#10b981', to: '#059669', glow: 'rgba(16, 185, 129, 0.5)' }; // green
    if (score >= 70) return { from: '#3b82f6', to: '#2563eb', glow: 'rgba(59, 130, 246, 0.5)' }; // blue
    if (score >= 55) return { from: '#f59e0b', to: '#d97706', glow: 'rgba(245, 158, 11, 0.5)' }; // orange
    return { from: '#ef4444', to: '#dc2626', glow: 'rgba(239, 68, 68, 0.5)' }; // red
  };

  const color = getColor();

  return (
    <div className="relative" style={{ width: size, height: size }}>
      {/* Background circle */}
      <svg className="transform -rotate-90" width={size} height={size}>
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="rgba(100, 116, 139, 0.2)"
          strokeWidth="16"
          fill="none"
        />
        {/* Progress circle */}
        <motion.circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={`url(#gradient-${score})`}
          strokeWidth="16"
          fill="none"
          strokeLinecap="round"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: circumference - progress }}
          transition={{ duration: 1.5, ease: 'easeOut' }}
          style={{ filter: `drop-shadow(0 0 8px ${color.glow})` }}
        />
        <defs>
          <linearGradient id={`gradient-${score}`} x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor={color.from} />
            <stop offset="100%" stopColor={color.to} />
          </linearGradient>
        </defs>
      </svg>

      {/* Score text */}
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <motion.div
          initial={{ scale: 0.5, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ delay: 0.5, duration: 0.5 }}
          className="text-center"
        >
          <div className="text-5xl font-bold text-gray-900 mb-1">
            {animatedScore}
          </div>
          <div className="text-sm text-gray-600 font-medium">
            out of 100
          </div>
        </motion.div>
      </div>

      {/* Glow effect */}
      <div
        className="absolute inset-0 rounded-full blur-2xl opacity-20"
        style={{
          background: `radial-gradient(circle, ${color.from} 0%, transparent 70%)`
        }}
      />
    </div>
  );
}
