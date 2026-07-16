import { create } from 'zustand';

export interface Alert {
  id: number;
  timestamp: string;
  src_ip: string;
  dest_ip: string;
  signature: string;
  severity: string;
  status: string;
  [key: string]: any;
}

interface AlertStore {
  alerts: Alert[];
  addAlerts: (newAlerts: Alert[]) => void;
  clearAlerts: () => void;
}

export const useAlertStore = create<AlertStore>((set) => ({
  alerts: [],
  addAlerts: (newAlerts) =>
    set((state) => {
      // Prepend new alerts and keep only the latest 1000 to prevent memory leaks
      const combined = [...newAlerts, ...state.alerts];
      return { alerts: combined.slice(0, 1000) };
    }),
  clearAlerts: () => set({ alerts: [] }),
}));
