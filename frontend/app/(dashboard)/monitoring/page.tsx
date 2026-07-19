'use client';

/**
 * System Monitoring — live health and traffic metrics for the NIDS pipeline.
 *
 * Wired to the existing /statistics/current and /system/health endpoints and
 * polled on a short interval so the numbers stay current without a WebSocket.
 */
import { useCallback, useEffect, useState } from 'react';
import api from '@/lib/api';
import type { ApiResponse } from '@/types/api';

interface TrafficStats {
  id: number;
  timestamp: string;
  alerts_total: number;
  alerts_critical: number;
  alerts_high: number;
  bytes_in: number;
  bytes_out: number;
  packets_in: number;
  packets_out: number;
}

const REFRESH_MS = 10_000;

function formatBytes(bytes: number): string {
  if (bytes <= 0) return '0 B';
  const units = ['B', 'KB', 'MB', 'GB', 'TB'];
  const exp = Math.min(Math.floor(Math.log(bytes) / Math.log(1024)), units.length - 1);
  return `${(bytes / 1024 ** exp).toFixed(exp === 0 ? 0 : 1)} ${units[exp]}`;
}

function formatNumber(value: number): string {
  return new Intl.NumberFormat().format(value);
}

function MetricCard({ label, value, hint }: { label: string; value: string; hint?: string }) {
  return (
    <div className="rounded-xl border border-border bg-card p-6 shadow-sm">
      <p className="text-sm font-medium text-muted-foreground">{label}</p>
      <p className="mt-2 text-3xl font-semibold tracking-tight">{value}</p>
      {hint && <p className="mt-1 text-xs text-muted-foreground">{hint}</p>}
    </div>
  );
}

export default function MonitoringPage() {
  const [stats, setStats] = useState<TrafficStats | null>(null);
  const [healthy, setHealthy] = useState<boolean | null>(null);
  const [loading, setLoading] = useState(true);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);

  const fetchMetrics = useCallback(async () => {
    try {
      const [statsRes, healthRes] = await Promise.allSettled([
        api.get<ApiResponse<TrafficStats>>('/statistics/current'),
        api.get<{ status: string }>('/system/health'),
      ]);

      if (statsRes.status === 'fulfilled') {
        setStats(statsRes.value.data.data);
      }
      setHealthy(
        healthRes.status === 'fulfilled' && healthRes.value.data.status === 'ok'
      );
      setLastUpdated(new Date());
    } catch (e) {
      console.error('Failed to fetch monitoring metrics', e);
      setHealthy(false);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchMetrics();
    const interval = setInterval(fetchMetrics, REFRESH_MS);
    return () => clearInterval(interval);
  }, [fetchMetrics]);

  return (
    <div className="flex flex-col space-y-6">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">System Monitoring</h2>
          <p className="text-muted-foreground">Live health and traffic metrics for NIDS components.</p>
        </div>
        <div className="flex flex-col items-end gap-1">
          <div className="flex items-center gap-2 rounded-md border border-border bg-card px-3 py-1.5">
            <span
              className={`h-2 w-2 rounded-full ${
                healthy === null
                  ? 'bg-muted-foreground'
                  : healthy
                    ? 'bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.6)]'
                    : 'bg-red-500 shadow-[0_0_8px_rgba(239,68,68,0.6)]'
              }`}
            />
            <span className="text-xs font-medium uppercase tracking-widest">
              {healthy === null ? 'Checking' : healthy ? 'Engine Online' : 'Engine Unreachable'}
            </span>
          </div>
          {lastUpdated && (
            <span className="text-xs text-muted-foreground">
              Updated {lastUpdated.toLocaleTimeString()}
            </span>
          )}
        </div>
      </div>

      {loading && !stats ? (
        <div className="rounded-xl border border-border bg-card p-8 text-center text-muted-foreground">
          Loading live metrics...
        </div>
      ) : (
        <>
          <section>
            <h3 className="mb-3 text-sm font-semibold uppercase tracking-widest text-muted-foreground">
              Traffic Throughput
            </h3>
            <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
              <MetricCard label="Packets In" value={formatNumber(stats?.packets_in ?? 0)} />
              <MetricCard label="Packets Out" value={formatNumber(stats?.packets_out ?? 0)} />
              <MetricCard label="Bytes In" value={formatBytes(stats?.bytes_in ?? 0)} />
              <MetricCard label="Bytes Out" value={formatBytes(stats?.bytes_out ?? 0)} />
            </div>
          </section>

          <section>
            <h3 className="mb-3 text-sm font-semibold uppercase tracking-widest text-muted-foreground">
              Alert Volume
            </h3>
            <div className="grid gap-4 sm:grid-cols-3">
              <MetricCard label="Total Alerts" value={formatNumber(stats?.alerts_total ?? 0)} />
              <MetricCard
                label="Critical"
                value={formatNumber(stats?.alerts_critical ?? 0)}
                hint="Highest-priority detections"
              />
              <MetricCard
                label="High"
                value={formatNumber(stats?.alerts_high ?? 0)}
                hint="Elevated-priority detections"
              />
            </div>
          </section>

          <p className="text-xs text-muted-foreground">
            Metrics refresh automatically every {REFRESH_MS / 1000} seconds from the latest
            statistics snapshot.
          </p>
        </>
      )}
    </div>
  );
}
