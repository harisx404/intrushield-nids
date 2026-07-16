'use client';

import { PageWrapper } from '@/components/layout/PageWrapper';

export default function SettingsPage() {
  return (
    <PageWrapper>
      <div className="flex flex-col space-y-6">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Settings</h2>
          <p className="text-muted-foreground">Manage your NIDS configuration and preferences.</p>
        </div>
        
        <div className="grid gap-6 md:grid-cols-2">
          <div className="rounded-xl border border-border bg-card p-6 shadow-sm">
            <h3 className="text-lg font-medium mb-4">Response Handlers</h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium">Slack Webhook</p>
                  <p className="text-sm text-muted-foreground">Send HIGH/CRITICAL alerts to Slack</p>
                </div>
                <button className="bg-secondary text-secondary-foreground px-3 py-1 rounded-md text-sm font-medium">Configure</button>
              </div>
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium">Email Notifications</p>
                  <p className="text-sm text-muted-foreground">Email admin on CRITICAL alerts</p>
                </div>
                <button className="bg-secondary text-secondary-foreground px-3 py-1 rounded-md text-sm font-medium">Configure</button>
              </div>
            </div>
          </div>

          <div className="rounded-xl border border-border bg-card p-6 shadow-sm">
            <h3 className="text-lg font-medium mb-4">Suricata Engine</h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium">Engine Status</p>
                  <p className="text-sm text-green-500 font-medium">Running</p>
                </div>
                <div className="space-x-2">
                  <button className="bg-secondary text-secondary-foreground px-3 py-1 rounded-md text-sm font-medium">Restart</button>
                  <button className="bg-secondary text-secondary-foreground px-3 py-1 rounded-md text-sm font-medium">Reload Rules</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </PageWrapper>
  );
}
