"use client";

import { useState } from "react";
import { coach } from "@/lib/api";

export default function Home() {
  const [exercise, setExercise] = useState("");
  const [description, setDescription] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await coach({ exercise, description });
      setResult(response);
    } catch (err: any) {
      setError(err.message ?? "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-gray-100 p-8">
      <div className="mx-auto max-w-xl rounded bg-white p-6 shadow">
        <h1 className="mb-4 text-2xl font-bold">AI Strength Coach</h1>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium">Exercise</label>
            <input
              className="mt-1 w-full rounded border p-2"
              value={exercise}
              onChange={(e) => setExercise(e.target.value)}
              placeholder="Back squat"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium">
              How did it feel?
            </label>
            <textarea
              className="mt-1 w-full rounded border p-2"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="My knees cave in at the bottom"
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded bg-blue-600 py-2 font-semibold text-white hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? "Analyzing..." : "Get coaching"}
          </button>
        </form>

        {error && (
          <p className="mt-4 rounded bg-red-100 p-2 text-red-700">
            {error}
          </p>
        )}

        {result && (
          <pre className="mt-4 overflow-auto rounded bg-gray-900 p-4 text-sm text-green-200">
            {JSON.stringify(result, null, 2)}
          </pre>
        )}
      </div>
    </main>
  );
}
