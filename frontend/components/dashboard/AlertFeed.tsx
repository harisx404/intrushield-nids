'use client';

import { useAlertStore } from '@/stores/alertStore';
import { AlertBadge } from '../ui/AlertBadge';
import { format } from 'date-fns';

export function AlertFeed() {
  const alerts = useAlertStore((state) => state.alerts);
  const displayAlerts = alerts.slice(0, 50);

  if (displayAlerts.length === 0) {
    return (
      <div className="h-full flex items-center justify-center border-2 border-dashed border-border rounded-lg bg-muted/10">
        <p className="text-sm text-muted-foreground px-4 text-center">No recent alerts detected. Listening for traffic...</p>
      </div>
    );
  }

  return (
    <div className="h-full overflow-y-auto pr-2 space-y-3">
      {displayAlerts.map((alert) => (
        <div key={alert.id} className="p-3 rounded-lg border border-border bg-background hover:bg-muted/30 transition-colors">
          <div className="flex items-start justify-between mb-2">
            <span className="font-medium text-sm truncate max-w-[70%]">{alert.signature}</span>
            <AlertBadge severity={alert.severity} />
          </div>
          <div className="flex justify-between text-xs text-muted-foreground">
            <span>{alert.src_ip} &rarr; {alert.dest_ip}</span>
            <span>{alert.timestamp ? format(new Date(alert.timestamp), 'HH:mm:ss') : 'Unknown Time'}</span>
          </div>
        </div>
      ))}
    </div>
  );
}
