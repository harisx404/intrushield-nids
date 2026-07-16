import { ReactNode } from 'react';

interface StatCardProps {
  title: string;
  value: string | number;
  icon: ReactNode;
  trend?: {
    value: string;
    isPositive: boolean;
  };
}

export function StatCard({ title, value, icon, trend }: StatCardProps) {
  return (
    <div className="rounded-xl border border-border bg-card p-6 shadow-sm">
      <div className="flex items-center justify-between">
        <p className="text-sm font-medium text-muted-foreground">{title}</p>
        <div className="text-muted-foreground">{icon}</div>
      </div>
      <div className="mt-4 flex items-baseline">
        <p className="text-3xl font-semibold">{value}</p>
        {trend && (
          <span className={`ml-2 text-sm font-medium ${trend.isPositive ? 'text-green-500' : 'text-red-500'}`}>
            {trend.value}
          </span>
        )}
      </div>
    </div>
  );
}
