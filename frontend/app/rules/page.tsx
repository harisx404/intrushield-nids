'use client';

import { useState, useEffect } from 'react';
import { PageWrapper } from '@/components/layout/PageWrapper';
import { api } from '@/lib/api';

type Rule = {
  id: number;
  sid: number;
  name: string;
  content: string;
  enabled: boolean;
};

export default function RulesPage() {
  const [rules, setRules] = useState<Rule[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRules = async () => {
      try {
        const res = await api.get('/rules');
        if (res.data.success) {
          setRules(res.data.data);
        }
      } catch (e) {
        console.error("Failed to fetch rules", e);
      } finally {
        setLoading(false);
      }
    };
    fetchRules();
  }, []);

  return (
    <PageWrapper>
      <div className="flex flex-col space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-bold tracking-tight">Detection Rules</h2>
            <p className="text-muted-foreground">Manage custom Suricata signatures.</p>
          </div>
          <button className="bg-primary text-primary-foreground px-4 py-2 rounded-md font-medium text-sm hover:bg-primary/90 transition-colors">
            Add New Rule
          </button>
        </div>

        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {loading ? (
            <div className="col-span-full p-8 text-center text-muted-foreground">Loading rules...</div>
          ) : rules.length === 0 ? (
            <div className="col-span-full p-8 text-center border-2 border-dashed border-border rounded-xl">
              <p className="text-muted-foreground">No custom rules configured yet.</p>
            </div>
          ) : (
            rules.map((rule) => (
              <div key={rule.id} className="border border-border bg-card rounded-xl p-5 flex flex-col shadow-sm">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="font-semibold text-lg truncate" title={rule.name}>{rule.name}</h3>
                    <p className="text-xs text-muted-foreground mt-1">SID: {rule.sid}</p>
                  </div>
                  <span className={`px-2 py-1 rounded text-xs font-medium ${rule.enabled ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400' : 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300'}`}>
                    {rule.enabled ? 'Enabled' : 'Disabled'}
                  </span>
                </div>
                <div className="flex-1 bg-muted/30 p-3 rounded-md overflow-hidden text-xs font-mono text-muted-foreground break-all">
                  {rule.content.length > 100 ? `${rule.content.substring(0, 100)}...` : rule.content}
                </div>
                <div className="mt-4 flex space-x-2">
                  <button className="flex-1 bg-secondary text-secondary-foreground py-2 rounded-md text-sm font-medium hover:bg-secondary/80">
                    Edit
                  </button>
                  <button className="px-3 bg-secondary text-destructive py-2 rounded-md text-sm font-medium hover:bg-destructive/10">
                    Delete
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </PageWrapper>
  );
}
