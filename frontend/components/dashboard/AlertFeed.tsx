'use client';

import { useEffect } from 'react';
import { useAlertStore, type Alert } from '@/stores/alertStore';
import api from '@/lib/api';
import type { PaginatedResponse } from '@/types/api';
import { format } from 'date-fns';

const getSeverityStyle = (severity: string) => {
  if (severity === 'CRITICAL' || severity === 'HIGH') return "px-2 py-0.5 rounded bg-secondary-container/20 text-secondary-container border border-secondary-container/30";
  if (severity === 'MEDIUM') return "px-2 py-0.5 rounded bg-tertiary-fixed-dim/20 text-tertiary-fixed-dim border border-tertiary-fixed-dim/30";
  return "px-2 py-0.5 rounded bg-primary-fixed-dim/20 text-primary-fixed-dim border border-primary-fixed-dim/30";
};

const getSeverityLabel = (severity: string) => {
  return severity; // It's already the right string, maybe just return it
};

export function AlertFeed() {
  const alerts = useAlertStore((state) => state.alerts);
  const setAlerts = useAlertStore((state) => state.setAlerts);
  const displayAlerts = alerts.slice(0, 50);

  // Seed the feed with the most recent alerts so it is populated on load;
  // the websocket then prepends live alerts on top of this baseline.
  useEffect(() => {
    let cancelled = false;
    const seedFeed = async () => {
      try {
        const res = await api.get<PaginatedResponse<Alert>>(
          '/alerts?page=1&per_page=50'
        );
        if (!cancelled && res.data.data) {
          setAlerts(res.data.data);
        }
      } catch {
        // Non-fatal: the feed will still fill from the live websocket stream.
      }
    };
    seedFeed();
    return () => {
      cancelled = true;
    };
  }, [setAlerts]);

  return (
    <div className="glass-panel rounded-lg overflow-hidden flex flex-col h-full border border-outline-variant/30">
      <div className="p-panel-padding border-b border-outline-variant/20 flex justify-between items-center">
        <div className="flex items-center gap-2">
          <span className="material-symbols-outlined text-primary-fixed-dim">stream</span>
          <h2 className="font-headline-sm text-[18px] font-semibold">Live Alert Feed</h2>
        </div>
        <div className="flex gap-2">
          <button className="font-label-caps text-[10px] px-2 py-1 rounded border border-outline-variant/50 hover:bg-surface-variant transition-colors">Export CSV</button>
          <button className="font-label-caps text-[10px] px-2 py-1 rounded bg-surface-container-highest border border-outline-variant/30 text-primary-fixed-dim hover:bg-surface-variant transition-colors">Live Sync</button>
        </div>
      </div>
      
      <div className="flex-1 overflow-y-auto max-h-[400px]">
        {displayAlerts.length === 0 ? (
          <div className="h-48 flex items-center justify-center">
            <p className="text-sm text-on-surface-variant px-4 text-center">No recent alerts detected. Listening for traffic...</p>
          </div>
        ) : (
          <table className="w-full text-left border-collapse">
            <thead className="sticky top-0 bg-surface-container font-label-caps text-[11px] text-on-surface-variant z-10 shadow-sm">
              <tr>
                <th className="p-4 border-b border-outline-variant/20">Timestamp</th>
                <th className="p-4 border-b border-outline-variant/20">Signature ID</th>
                <th className="p-4 border-b border-outline-variant/20">Severity</th>
                <th className="p-4 border-b border-outline-variant/20">Source IP</th>
                <th className="p-4 border-b border-outline-variant/20 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="font-code-sm text-[12px] divide-y divide-outline-variant/10">
              {displayAlerts.map((alert) => (
                <tr key={alert.id} className="hover:bg-white/5 transition-colors cursor-pointer group">
                  <td className="p-4 text-on-surface-variant group-hover:text-on-surface">
                    {alert.timestamp ? format(new Date(alert.timestamp), 'HH:mm:ss:SSS') : 'N/A'}
                  </td>
                  <td className="p-4 text-on-surface font-medium truncate max-w-[200px]">{alert.signature}</td>
                  <td className="p-4">
                    <span className={getSeverityStyle(alert.severity)}>
                      {getSeverityLabel(alert.severity)}
                    </span>
                  </td>
                  <td className="p-4 text-on-surface-variant">{alert.src_ip}</td>
                  <td className="p-4 text-right">
                    <span className="material-symbols-outlined text-on-surface-variant cursor-pointer hover:text-primary-fixed-dim transition-colors">more_horiz</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
