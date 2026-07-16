'use client';

import { useEffect, useState } from 'react';
import { useWebSocket } from '@/hooks/useWebSocket';
import { AlertBadge } from '../ui/AlertBadge';
import { format } from 'date-fns';

type Alert = {
  id: number;
  timestamp: string;
  signature: string;
  severity: string;
  src_ip: string;
  dest_ip: string;
};

export function AlertFeed() {
  const { lastMessage } = useWebSocket();
  const [alerts, setAlerts] = useState<Alert[]>([]);

  useEffect(() => {
    if (lastMessage?.event === 'new_alert') {
      const newAlert = lastMessage.data.alert;
      setAlerts(prev => [
        {
          id: lastMessage.data.alert_id,
          timestamp: newAlert.timestamp,
          signature: newAlert.signature,
          severity: newAlert.severity,
          src_ip: newAlert.src_ip,
          dest_ip: newAlert.dest_ip,
        },
        ...prev
      ].slice(0, 50));
    }
  }, [lastMessage]);

  if (alerts.length === 0) {
    return (
      <div className="h-full flex items-center justify-center border-2 border-dashed border-border rounded-lg bg-muted/10">
        <p className="text-sm text-muted-foreground px-4 text-center">No recent alerts detected. Listening for traffic...</p>
      </div>
    );
  }

  return (
    <div className="h-full overflow-y-auto pr-2 space-y-3">
      {alerts.map((alert) => (
        <div key={alert.id} className="p-3 rounded-lg border border-border bg-background hover:bg-muted/30 transition-colors">
          <div className="flex items-start justify-between mb-2">
            <span className="font-medium text-sm truncate max-w-[70%]">{alert.signature}</span>
            <AlertBadge severity={alert.severity} />
          </div>
          <div className="flex justify-between text-xs text-muted-foreground">
            <span>{alert.src_ip} &rarr; {alert.dest_ip}</span>
            <span>{format(new Date(alert.timestamp), 'HH:mm:ss')}</span>
          </div>
        </div>
      ))}
    </div>
  );
}
