'use client';

import { useEffect } from 'react';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log the error to an error reporting service
    console.error('Application Error Boundary Caught:', error);
  }, [error]);

  return (
    <div className="flex h-screen w-full flex-col items-center justify-center bg-zinc-950 text-white">
      <div className="flex max-w-md flex-col items-center space-y-4 text-center">
        <h2 className="text-2xl font-bold text-red-500">Something went wrong!</h2>
        <p className="text-zinc-400">
          A critical error occurred in the dashboard component. Please try reloading.
        </p>
        <button
          onClick={() => reset()}
          className="rounded-md bg-blue-600 px-4 py-2 font-medium text-white hover:bg-blue-700 transition-colors"
        >
          Try again
        </button>
      </div>
    </div>
  );
}
