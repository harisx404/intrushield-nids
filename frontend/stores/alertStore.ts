import { create } from 'zustand';

export interface Alert {
  id: number;
  timestamp: string;
  src_ip: string;
  dst_ip: string;
  signature: string;
  severity: string;
  status: string;
  [key: string]: any;
}

interface AlertStore {
  alerts: Alert[];
  /** Prepend live alerts arriving over the websocket. */
  addAlerts: (newAlerts: Alert[]) => void;
  /** Replace the feed with an initial page fetched over REST. */
  setAlerts: (alerts: Alert[]) => void;
  clearAlerts: () => void;
}

const MAX_ALERTS = 1000;

/** Deduplicate by id, preserving order (first occurrence wins). */
const dedupeById = (alerts: Alert[]): Alert[] => {
  const seen = new Set<number>();
  const result: Alert[] = [];
  for (const alert of alerts) {
    if (seen.has(alert.id)) continue;
    seen.add(alert.id);
    result.push(alert);
  }
  return result;
};

export const useAlertStore = create<AlertStore>((set) => ({
  alerts: [],
  addAlerts: (newAlerts) =>
    set((state) => ({
      // Prepend new alerts, drop duplicates, and cap the buffer to avoid leaks.
      alerts: dedupeById([...newAlerts, ...state.alerts]).slice(0, MAX_ALERTS),
    })),
  setAlerts: (alerts) => set({ alerts: dedupeById(alerts).slice(0, MAX_ALERTS) }),
  clearAlerts: () => set({ alerts: [] }),
}));
