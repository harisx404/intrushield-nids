import { useEffect, useRef, useState, useCallback } from 'react';
import { CONSTANTS } from '../lib/constants';
import { useAlertStore, Alert } from '../stores/alertStore';

export type WebSocketMessage = {
  type: string;
  data: any;
};

export const useWebSocket = () => {
  const [isConnected, setIsConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout>();
  
  // High-performance buffer to hold incoming messages before flushing
  const messageBuffer = useRef<Alert[]>([]);
  const flushIntervalRef = useRef<NodeJS.Timeout>();

  const addAlerts = useAlertStore((state) => state.addAlerts);

  const connect = useCallback(() => {
    try {
      const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
      const wsUrl = `${CONSTANTS.WS_URL}?token=${token || ''}`;
      
      const ws = new WebSocket(wsUrl);

      ws.onopen = () => {
        setIsConnected(true);
      };

      ws.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data);
          if (message.type === "new_alert" && message.data) {
             messageBuffer.current.push(message.data);
          }
        } catch (e) {
          console.error("Failed to parse WS message", e);
        }
      };

      ws.onclose = () => {
        setIsConnected(false);
        // Attempt to reconnect after 3 seconds
        reconnectTimeoutRef.current = setTimeout(() => {
          connect();
        }, 3000);
      };

      wsRef.current = ws;
    } catch (e) {
      console.error("Failed to setup WebSocket", e);
    }
  }, []);

  useEffect(() => {
    connect();

    // Flush buffer every 100ms (debouncing React renders)
    flushIntervalRef.current = setInterval(() => {
      if (messageBuffer.current.length > 0) {
        addAlerts([...messageBuffer.current]);
        messageBuffer.current = []; // Clear buffer
      }
    }, 100);

    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      if (flushIntervalRef.current) {
        clearInterval(flushIntervalRef.current);
      }
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [connect, addAlerts]);

  return { isConnected };
};
