'use client';

import { Bell, User } from 'lucide-react';
import { useWebSocket } from '@/hooks/useWebSocket';

export function Header() {
  const { isConnected } = useWebSocket();

  return (
    <header className="flex h-16 items-center justify-between border-b border-border bg-card px-6">
      <div className="flex items-center">
        <h1 className="text-xl font-semibold">Security Operations Center</h1>
      </div>
      <div className="flex items-center space-x-4">
        <div className="flex items-center mr-4">
          <span className={`h-2.5 w-2.5 rounded-full mr-2 ${isConnected ? 'bg-green-500' : 'bg-red-500 animate-pulse'}`}></span>
          <span className="text-sm text-muted-foreground">{isConnected ? 'Live' : 'Disconnected'}</span>
        </div>
        <button className="text-muted-foreground hover:text-foreground">
          <Bell className="h-5 w-5" />
        </button>
        <div className="flex items-center space-x-2">
          <div className="h-8 w-8 rounded-full bg-secondary flex items-center justify-center">
            <User className="h-5 w-5 text-muted-foreground" />
          </div>
        </div>
      </div>
    </header>
  );
}
