'use client';

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <html lang="en">
      <body>
        <div className="flex h-screen w-full flex-col items-center justify-center bg-zinc-950 text-white">
          <div className="flex max-w-md flex-col items-center space-y-4 text-center">
            <h2 className="text-3xl font-bold text-red-500">Fatal Application Error</h2>
            <p className="text-zinc-400">
              The application encountered a fatal error and could not render the root layout.
            </p>
            <button
              onClick={() => reset()}
              className="rounded-md bg-red-600 px-4 py-2 font-medium text-white hover:bg-red-700 transition-colors"
            >
              Force Reload
            </button>
          </div>
        </div>
      </body>
    </html>
  );
}
