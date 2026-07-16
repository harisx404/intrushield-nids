import { CONSTANTS } from '@/lib/constants';

interface AlertBadgeProps {
  severity: string;
}

export function AlertBadge({ severity }: AlertBadgeProps) {
  let colorClass = 'bg-gray-100 text-gray-800 dark:bg-gray-800/50 dark:text-gray-300';
  
  switch (severity?.toUpperCase()) {
    case CONSTANTS.SEVERITY_LEVELS.CRITICAL:
      colorClass = 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400 border border-red-200 dark:border-red-800/50';
      break;
    case CONSTANTS.SEVERITY_LEVELS.HIGH:
      colorClass = 'bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-400 border border-orange-200 dark:border-orange-800/50';
      break;
    case CONSTANTS.SEVERITY_LEVELS.MEDIUM:
      colorClass = 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400 border border-yellow-200 dark:border-yellow-800/50';
      break;
    case CONSTANTS.SEVERITY_LEVELS.LOW:
      colorClass = 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400 border border-blue-200 dark:border-blue-800/50';
      break;
    case CONSTANTS.SEVERITY_LEVELS.INFO:
      colorClass = 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400 border border-green-200 dark:border-green-800/50';
      break;
  }

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${colorClass}`}>
      {severity}
    </span>
  );
}
