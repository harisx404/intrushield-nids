'use client';

import { useEffect, useState } from 'react';
import { PageWrapper } from '@/components/layout/PageWrapper';
import { StatCard } from '@/components/ui/StatCard';
import { AlertFeed } from '@/components/dashboard/AlertFeed';
import { ShieldAlert, AlertTriangle, Activity, CheckCircle2 } from 'lucide-react';
import { api } from '@/lib/api';

export default function Dashboard() {
  const [stats, setStats] = useState({
    total: 0,
    critical: 0,
    high: 0,
    today: 0
  });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await api.get('/statistics/summary');
        if (res.data.success) {
          setStats(res.data.data);
        }
      } catch (e) {
        console.error("Failed to fetch stats", e);
      }
    };
    fetchStats();
  }, []);

  return (
    <PageWrapper>
      <div className="flex flex-col space-y-6">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Dashboard</h2>
          <p className="text-muted-foreground">Real-time overview of network security.</p>
        </div>

        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <StatCard
            title="Total Alerts"
            value={stats.total.toLocaleString()}
            icon={<ShieldAlert className="h-5 w-5 text-blue-500" />}
          />
          <StatCard
            title="Critical Threats"
            value={stats.critical.toLocaleString()}
            icon={<AlertTriangle className="h-5 w-5 text-red-500" />}
            trend={{ value: '+2', isPositive: false }}
          />
          <StatCard
            title="High Severity"
            value={stats.high.toLocaleString()}
            icon={<Activity className="h-5 w-5 text-orange-500" />}
          />
          <StatCard
            title="System Status"
            value="Active"
            icon={<CheckCircle2 className="h-5 w-5 text-green-500" />}
          />
        </div>

        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
          <div className="col-span-4 rounded-xl border border-border bg-card p-6 shadow-sm">
            <h3 className="text-lg font-medium mb-4">Traffic Timeline</h3>
            <div className="h-[300px] flex items-center justify-center bg-muted/20 rounded-md">
              <span className="text-muted-foreground text-sm">Traffic Timeline Chart Placeholder</span>
            </div>
          </div>
          <div className="col-span-3 rounded-xl border border-border bg-card p-6 shadow-sm flex flex-col h-[400px]">
            <h3 className="text-lg font-medium mb-4">Live Alert Feed</h3>
            <div className="flex-1 overflow-hidden">
              <AlertFeed />
            </div>
          </div>
        </div>
      </div>
    </PageWrapper>
  );
}
