import { useState } from "react"

export default function App() {
  const [formData, setFormData] = useState({
    origin_airport: "",
    destination_country: "",
    departure_date: "",
    return_date: "",
    passengers: "",
    max_budget: ""
  })

  const [step, setStep] = useState("form") // form | flights | houses | completed
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const [flightOptions, setFlightOptions] = useState([])
  const [selectedFlight, setSelectedFlight] = useState(null)

  const [houseOptions, setHouseOptions] = useState([])
  const [selectedHouse, setSelectedHouse] = useState(null)

  const [finalPlan, setFinalPlan] = useState(null)

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  // STEP 1 → START
  const startTravel = async () => {
    setLoading(true)
    setError(null)

    try {
      const response = await fetch("http://127.0.0.1:8000/travel/start", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...formData,
          passengers: parseInt(formData.passengers),
          max_budget: parseFloat(formData.max_budget)
        })
      })

      const data = await response.json()

      if (!response.ok) throw new Error("Error en backend")

      setFlightOptions(data.flightOptions || data.flight_options)
      setStep("flights")
    } catch (err) {
      setError("Error iniciando planificación")
    } finally {
      setLoading(false)
    }
  }

  // STEP 2 → SELECT FLIGHT
  const chooseFlight = async (flight) => {
    setLoading(true)
    setSelectedFlight(flight)

    try {
      const response = await fetch("http://127.0.0.1:8000/travel/select-flight", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_request: {
            ...formData,
            passengers: parseInt(formData.passengers),
            max_budget: parseFloat(formData.max_budget)
          },
          selected_flight_id: flight.id,
          flight_options: flightOptions
        })
      })

      const data = await response.json()

      setHouseOptions(data.house_options)
      setStep("houses")
    } catch (err) {
      setError("Error seleccionando vuelo")
    } finally {
      setLoading(false)
    }
  }

  // STEP 3 → SELECT HOUSE
  const chooseHouse = async (house) => {
    setLoading(true)
    setSelectedHouse(house)

    try {
      const response = await fetch("http://127.0.0.1:8000/travel/select-house", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_request: {
            ...formData,
            passengers: parseInt(formData.passengers),
            max_budget: parseFloat(formData.max_budget)
          },
          selected_flight: selectedFlight,
          selected_house_id: house.id,
          house_options: houseOptions
        })
      })

      const data = await response.json()
      setFinalPlan(data.travel_plan)
      setStep("completed")
    } catch (err) {
      setError("Error generando plan final")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <h1>🌍 Travel Planner MVP</h1>

      {step === "form" && (
        <div>
          <input name="origin_airport" placeholder="Origen" onChange={handleInputChange} />
          <input name="destination_country" placeholder="Destino" onChange={handleInputChange} />
          <input type="date" name="departure_date" onChange={handleInputChange} />
          <input type="date" name="return_date" onChange={handleInputChange} />
          <input type="number" name="passengers" placeholder="Pasajeros" onChange={handleInputChange} />
          <input type="number" name="max_budget" placeholder="Presupuesto" onChange={handleInputChange} />
          <button onClick={startTravel} disabled={loading}>
            {loading ? "Buscando vuelos..." : "Buscar vuelos"}
          </button>
        </div>
      )}

      {step === "flights" && (
        <div>
          <h2>Selecciona un vuelo</h2>
          {flightOptions.map(f => (
            <div key={f.id} className="card">
              <p><strong>{f.airline}</strong> - €{f.price}</p>
              <button onClick={() => chooseFlight(f)}>Seleccionar</button>
            </div>
          ))}
        </div>
      )}

      {step === "houses" && (
        <div>
          <h2>Selecciona alojamiento</h2>
          {houseOptions.map(h => (
            <div key={h.id} className="card">
              <p><strong>{h.name}</strong> - €{h.total_price}</p>
              <button onClick={() => chooseHouse(h)}>Seleccionar</button>
            </div>
          ))}
        </div>
      )}

      {step === "completed" && (
        <div>
          <h2>📋 Plan Final</h2>
          <pre style={{ whiteSpace: "pre-wrap" }}>{finalPlan}</pre>
        </div>
      )}

      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  )
}
