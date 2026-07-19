'use client';

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from 'recharts';

const data = [
  { time: '00:00', alerts: 0, traffic: 120 },
  { time: '04:00', alerts: 2, traffic: 300 },
  { time: '08:00', alerts: 5, traffic: 800 },
  { time: '12:00', alerts: 1, traffic: 400 },
  { time: '16:00', alerts: 8, traffic: 950 },
  { time: '20:00', alerts: 3, traffic: 500 },
  { time: '24:00', alerts: 0, traffic: 150 },
];

export function TrafficChart() {
  return (
    <div className="h-full w-full">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          data={data}
          margin={{
            top: 5,
            right: 10,
            left: -20,
            bottom: 0,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#333" opacity={0.2} />
          <XAxis 
            dataKey="time" 
            axisLine={false}
            tickLine={false}
            tick={{ fontSize: 12 }}
            dy={10}
          />
          <YAxis 
            yAxisId="left"
            axisLine={false}
            tickLine={false}
            tick={{ fontSize: 12 }}
          />
          <YAxis 
            yAxisId="right"
            orientation="right"
            axisLine={false}
            tickLine={false}
            tick={{ fontSize: 12 }}
          />
          <Tooltip 
            contentStyle={{ 
              backgroundColor: 'var(--background)', 
              borderColor: 'var(--border)',
              borderRadius: '8px'
            }}
          />
          <Line 
            yAxisId="left"
            type="monotone" 
            dataKey="traffic" 
            stroke="#3b82f6" 
            strokeWidth={2}
            dot={false}
            activeDot={{ r: 6 }}
            name="Traffic (MB)"
          />
          <Line 
            yAxisId="right"
            type="monotone" 
            dataKey="alerts" 
            stroke="#ef4444" 
            strokeWidth={2}
            dot={false}
            activeDot={{ r: 6 }}
            name="Alerts"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
