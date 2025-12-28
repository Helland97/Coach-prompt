export type CoachingRequest = {
  exercise: string;
  description: string;
};

export async function coach(request: CoachingRequest) {
  const res = await fetch("http://localhost:8000/coach", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Backend error ${res.status}: ${text}`);
  }

  return res.json();
}
