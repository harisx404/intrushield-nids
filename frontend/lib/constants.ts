export const CONSTANTS = {
  API_BASE_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1',
  WS_URL: process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000/api/v1/ws',
  
  SEVERITY_LEVELS: {
    CRITICAL: 'CRITICAL',
    HIGH: 'HIGH',
    MEDIUM: 'MEDIUM',
    LOW: 'LOW',
    INFO: 'INFO',
  },
};
