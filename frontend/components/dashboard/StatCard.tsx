import React from 'react';

interface StatCardProps {
  title: string;
  value: number | string;
  icon: string;
  isLoading?: boolean;
  variant?: 'default' | 'critical' | 'amber' | 'cyan';
}

export function StatCard({ title, value, icon, isLoading, variant = 'default' }: StatCardProps) {
  let panelStyle = "glass-panel p-panel-padding rounded-lg flex flex-col justify-between h-32 relative overflow-hidden group";
  let iconStyle = "absolute -right-4 -top-4 opacity-10 group-hover:opacity-20 transition-opacity";
  let valueStyle = "font-headline-md text-[24px] font-bold text-on-surface";
  let barStyle = "h-full bg-surface-variant"; // default fallback
  let tagStyle = "font-label-caps text-[10px] flex items-center text-on-surface-variant";
  let tagText = "LIVE";
  
  if (variant === 'critical') {
    panelStyle += " border-secondary-container/30 critical-pulse";
    iconStyle += " text-secondary-container";
    valueStyle = "font-headline-md text-[24px] font-bold text-secondary-container";
    barStyle = "bg-secondary-container animate-pulse h-full";
    tagStyle = "font-label-caps text-[10px] flex items-center text-secondary-container";
    tagText = "URGENT";
  } else if (variant === 'amber') {
    iconStyle += " text-tertiary-fixed-dim";
    barStyle = "bg-tertiary-fixed-dim h-full";
    tagStyle = "font-label-caps text-[10px] flex items-center text-tertiary-fixed-dim";
    tagText = "MODIFIED";
  } else if (variant === 'cyan') {
    panelStyle += " inner-glow-cyan";
    iconStyle += " text-primary-fixed-dim";
    barStyle = "bg-primary-fixed-dim h-full";
    tagStyle = "font-label-caps text-[10px] flex items-center text-primary-fixed-dim";
    tagText = "LIVE";
  } else {
    // Default
    barStyle = "bg-primary-fixed-dim h-full";
  }

  // Simulate progress bar width based on value length to look dynamic
  const valNum = Number(value) || 0;
  const progressWidth = Math.min(100, Math.max(15, (valNum % 100) + 15)) + '%';

  return (
    <div className={panelStyle}>
      <div className={iconStyle}>
        <span className="material-symbols-outlined text-[96px]" style={{ fontVariationSettings: "'FILL' 1" }}>
          {icon}
        </span>
      </div>
      
      <div className="flex justify-between items-start z-10 relative">
        <span className="font-label-caps text-[11px] font-bold tracking-widest text-on-surface-variant uppercase">
          {title}
        </span>
        <span className={tagStyle}>{tagText}</span>
      </div>
      
      <div className="z-10 relative">
        <span className={valueStyle}>
          {isLoading ? '...' : value}
        </span>
        <div className="w-full h-1 bg-surface-variant rounded-full mt-2 overflow-hidden">
          <div className={barStyle} style={{ width: isLoading ? '0%' : progressWidth }}></div>
        </div>
      </div>
    </div>
  );
}
