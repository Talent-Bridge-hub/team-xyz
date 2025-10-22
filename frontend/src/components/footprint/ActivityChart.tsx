import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { motion } from 'framer-motion';

interface Scan {
  scanned_at: string;
  overall_score: number;
  github_score: number | null;
  stackoverflow_score: number | null;
  visibility_score: number;
  activity_score: number;
  impact_score: number;
  expertise_score: number;
}

interface ActivityChartProps {
  scanHistory: Scan[];
}

export default function ActivityChart({ scanHistory }: ActivityChartProps) {
  // Transform data for recharts
  const chartData = scanHistory
    .slice()
    .reverse()
    .map(scan => ({
      date: new Date(scan.scanned_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
      overall: scan.overall_score,
      visibility: scan.visibility_score,
      activity: scan.activity_score,
      impact: scan.impact_score,
      expertise: scan.expertise_score,
      github: scan.github_score || 0,
      stackoverflow: scan.stackoverflow_score || 0
    }));

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white border-2 border-gray-200 rounded-lg p-3 shadow-xl">
          <p className="text-gray-900 font-semibold mb-2">{label}</p>
          {payload.map((entry: any, index: number) => (
            <div key={index} className="flex items-center justify-between gap-3 text-sm">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full" style={{ backgroundColor: entry.color }} />
                <span className="text-gray-700">{entry.name}</span>
              </div>
              <span className="text-gray-900 font-bold">{Math.round(entry.value)}</span>
            </div>
          ))}
        </div>
      );
    }
    return null;
  };

  if (scanHistory.length === 0) {
    return (
      <div className="flex items-center justify-center h-64 text-gray-400">
        No scan history available
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ delay: 0.2 }}
      className="w-full h-80"
    >
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(209, 213, 219, 0.5)" />
          <XAxis
            dataKey="date"
            stroke="#6b7280"
            style={{ fontSize: '12px' }}
          />
          <YAxis
            stroke="#6b7280"
            style={{ fontSize: '12px' }}
            domain={[0, 100]}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend
            wrapperStyle={{ color: '#6b7280', fontSize: '12px' }}
            iconType="circle"
          />
          <Line
            type="monotone"
            dataKey="overall"
            stroke="#0ea5e9"
            strokeWidth={3}
            name="Overall Score"
            dot={{ fill: '#0ea5e9', r: 4 }}
            activeDot={{ r: 6 }}
          />
          <Line
            type="monotone"
            dataKey="visibility"
            stroke="#8b5cf6"
            strokeWidth={2}
            name="Visibility"
            dot={{ fill: '#8b5cf6', r: 3 }}
          />
          <Line
            type="monotone"
            dataKey="activity"
            stroke="#10b981"
            strokeWidth={2}
            name="Activity"
            dot={{ fill: '#10b981', r: 3 }}
          />
          <Line
            type="monotone"
            dataKey="impact"
            stroke="#f59e0b"
            strokeWidth={2}
            name="Impact"
            dot={{ fill: '#f59e0b', r: 3 }}
          />
          <Line
            type="monotone"
            dataKey="expertise"
            stroke="#ef4444"
            strokeWidth={2}
            name="Expertise"
            dot={{ fill: '#ef4444', r: 3 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </motion.div>
  );
}
