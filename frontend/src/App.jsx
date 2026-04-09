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
  const [reviewComment, setReviewComment] = useState("")

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

      // ✅ Caso: presupuesto insuficiente para alojamiento
      if (data.status === "no_accommodation_budget") {
        setError(data.message)
        setFlightOptions(data.flight_options)
        setStep("flights")
        return
      }

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

  const handleReview = async (type) => {
    try {
      const response = await fetch("http://127.0.0.1:8000/travel/review", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          type,
          comment: reviewComment,
          context: {
            user_request: formData,
            selected_flight: selectedFlight,
            selected_house: selectedHouse
          }
        })
      })

      const data = await response.json()

      // ✅ Editorial revision (regenerate final document)
      if (data.status === "revised") {
        setFinalPlan(data.travel_plan)
        setStep("completed")
      }

      // ✅ Re-run flight selection
      if (data.status === "pending_flight_selection") {
        setFlightOptions(data.flight_options)
        setStep("flights")
      }

      // ✅ Re-run house selection (CRITICAL FIX)
      if (data.status === "pending_house_selection") {
        setHouseOptions(data.house_options)
        setSelectedHouse(null)
        setFinalPlan(null)
        setStep("houses")
      }

      // ✅ If backend already finalized automatically
      if (data.status === "completed") {
        setFinalPlan(data.travel_plan)
        setStep("completed")
      }

    } catch (err) {
      console.error("Error in review", err)
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
          {flightOptions.map((f, index) => (
            <div
              key={f.id}
              className="card"
              style={{
                border: index === 0 ? "2px solid green" : "1px solid #ccc",
                padding: "12px",
                marginBottom: "12px",
                borderRadius: "8px"
              }}
            >
              <p><strong>{f.airline}</strong> - €{f.price}</p>
              <p>⭐ Score total: <strong>{f.score}</strong></p>
              <div style={{ background: "#eee", height: "8px", borderRadius: "4px", marginBottom: "8px" }}>
                <div
                  style={{
                    width: `${f.score}%`,
                    height: "8px",
                    background: "green",
                    borderRadius: "4px"
                  }}
                />
              </div>

              {index === 0 && <p style={{ color: "green" }}>🏆 Mejor opción calidad/precio</p>}

              {f.scoring_breakdown && (
                <div style={{ fontSize: "0.9em", marginBottom: "8px" }}>
                  <div>
                    💰 Precio: {f.scoring_breakdown.price_score.value} / {f.scoring_breakdown.price_score.max}
                  </div>
                  <div>
                    🛑 Escalas: {f.scoring_breakdown.stops_score.value} / {f.scoring_breakdown.stops_score.max}
                  </div>
                  <div>
                    ⏱ Duración: {f.scoring_breakdown.duration_score.value} / {f.scoring_breakdown.duration_score.max}
                  </div>
                  <div>
                    📊 Presupuesto: {f.scoring_breakdown.budget_alignment.value} / {f.scoring_breakdown.budget_alignment.max}
                  </div>
                </div>
              )}

              <button onClick={() => chooseFlight(f)}>Seleccionar</button>
            </div>
          ))}
        </div>
      )}

      {step === "houses" && (
        <div>
          <h2>Selecciona alojamiento</h2>
          {houseOptions.map((h, index) => (
            <div
              key={h.id}
              className="card"
              style={{
                border: index === 0 ? "2px solid green" : "1px solid #ccc",
                padding: "12px",
                marginBottom: "12px",
                borderRadius: "8px"
              }}
            >
              <p><strong>{h.name}</strong> - €{h.total_price}</p>
              <p>⭐ Score total: <strong>{h.score}</strong></p>
              <div style={{ background: "#eee", height: "8px", borderRadius: "4px", marginBottom: "8px" }}>
                <div
                  style={{
                    width: `${h.score}%`,
                    height: "8px",
                    background: "green",
                    borderRadius: "4px"
                  }}
                />
              </div>

              {index === 0 && <p style={{ color: "green" }}>🏆 Mejor alojamiento recomendado</p>}

              {h.scoring_breakdown && (
                <div style={{ fontSize: "0.9em", marginBottom: "8px" }}>
                  <div>
                    💰 Precio: {h.scoring_breakdown.price_score.value} / {h.scoring_breakdown.price_score.max}
                  </div>
                  <div>
                    ⭐ Rating: {h.scoring_breakdown.rating_score.value} / {h.scoring_breakdown.rating_score.max}
                  </div>
                  <div>
                    📝 Reviews: {h.scoring_breakdown.reviews_score.value} / {h.scoring_breakdown.reviews_score.max}
                  </div>
                  <div>
                    🏠 Amenities: {h.scoring_breakdown.amenities_score.value} / {h.scoring_breakdown.amenities_score.max}
                  </div>
                  <div>
                    📊 Presupuesto: {h.scoring_breakdown.budget_alignment.value} / {h.scoring_breakdown.budget_alignment.max}
                  </div>
                </div>
              )}

              <button onClick={() => chooseHouse(h)}>Seleccionar</button>
            </div>
          ))}
        </div>
      )}

      {step === "completed" && (
        <div>
          <h2>📋 Plan Final</h2>
          <pre style={{ whiteSpace: "pre-wrap" }}>{finalPlan}</pre>

          <div style={{ marginTop: "20px" }}>
            <h3>🧑 Revisión humana (HITL)</h3>
            <textarea
              placeholder="Añadir comentario o solicitar cambios..."
              value={reviewComment}
              onChange={(e) => setReviewComment(e.target.value)}
              style={{ width: "100%", height: "80px", marginBottom: "10px" }}
            />
            <button
              style={{ marginRight: "10px" }}
              onClick={() => handleReview("editorial")}
            >
              📝 Revisar redacción
            </button>
            <button onClick={() => handleReview("criteria")}>
              🔁 Cambiar criterios
            </button>
          </div>
        </div>
      )}

      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  )
}
