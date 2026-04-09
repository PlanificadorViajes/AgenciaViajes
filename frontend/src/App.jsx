import { useState } from "react"

export default function App() {
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const generatePlan = async () => {
    if (!input) return

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await fetch("http://127.0.0.1:8000/travel-request", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          user_input: input
        })
      })

      if (!response.ok) {
        throw new Error("API error")
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError("Failed to generate itinerary")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <h1>🌍 Travel Itinerary Generator</h1>

      <textarea
        placeholder="Describe your trip (e.g. 7 days in Japan with medium budget)"
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />

      <button onClick={generatePlan} disabled={loading}>
        {loading ? "Generating..." : "Generate Plan"}
      </button>

      {error && <p className="error">{error}</p>}

      {result && (
        <div className="result">
          <h2>Result</h2>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  )
}
