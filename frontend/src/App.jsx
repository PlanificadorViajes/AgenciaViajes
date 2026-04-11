import { useMemo, useState } from "react"

const API_URL = "http://127.0.0.1:8000"

const flightMetrics = [
  { key: "price_score", label: "💰 Precio" },
  { key: "stops_score", label: "✈️ Escalas" },
  { key: "duration_score", label: "⏱ Duración" },
  { key: "budget_alignment", label: "📊 Presupuesto" }
]

const houseMetrics = [
  { key: "price_score", label: "💰 Precio" },
  { key: "rating_score", label: "⭐ Rating" },
  { key: "reviews_score", label: "📝 Reviews" },
  { key: "amenities_score", label: "🏠 Amenities" },
  { key: "budget_alignment", label: "📊 Presupuesto" }
]

const ScoreBar = ({ score }) => (
  <div style={{ background: "#eee", height: "8px", borderRadius: "4px", marginBottom: "10px" }}>
    <div
      style={{
        width: `${Math.min(score, 100)}%`,
        height: "8px",
        borderRadius: "4px",
        background: score > 80 ? "#2ecc71" : score > 60 ? "#f1c40f" : "#e74c3c",
        transition: "width 0.3s ease"
      }}
    />
  </div>
)

const ScoreBadges = ({ breakdown, metrics }) => {
  if (!breakdown) return null

  return (
    <div className="score-badges">
      {metrics.map(({ key, label }) => {
        const metric = breakdown[key]
        if (!metric) return null
        return (
          <span key={key} className="score-badge">
            <strong>{label}:</strong> {metric.value} / {metric.max}
          </span>
        )
      })}
    </div>
  )
}

const StepIndicator = ({ step }) => {
  const steps = ["form", "flights", "houses", "completed"]
  const labels = {
    form: "Solicitud",
    flights: "Vuelos",
    houses: "Alojamientos",
    completed: "Plan final"
  }

  return (
    <div className="stepper">
      {steps.map((key, index) => (
        <div key={key} className={`step ${step === key ? "active" : steps.indexOf(step) > index ? "done" : ""}`}>
          <span>{index + 1}</span>
          <p>{labels[key]}</p>
        </div>
      ))}
    </div>
  )
}

export default function App() {
  const [formData, setFormData] = useState({
    origin_airport: "",
    destination_country: "",
    departure_date: "",
    return_date: "",
    passengers: "",
    max_budget: ""
  })

  const [step, setStep] = useState("form")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const [flightOptions, setFlightOptions] = useState([])
  const [selectedFlight, setSelectedFlight] = useState(null)

  const [houseOptions, setHouseOptions] = useState([])
  const [selectedHouse, setSelectedHouse] = useState(null)

  const [finalPlan, setFinalPlan] = useState(null)
  const [reviewComment, setReviewComment] = useState("")

  const requestPayload = useMemo(
    () => ({
      ...formData,
      passengers: parseInt(formData.passengers || "0", 10),
      max_budget: parseFloat(formData.max_budget || "0")
    }),
    [formData]
  )

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const startTravel = async () => {
    setLoading(true)
    setError(null)

    try {
      const response = await fetch(`${API_URL}/travel/start`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestPayload)
      })

      const data = await response.json()

      if (!response.ok) throw new Error(data?.message || "Error en backend")

      setFlightOptions(data.flightOptions || data.flight_options || [])
      setStep("flights")
    } catch (err) {
      setError("Error iniciando planificación")
    } finally {
      setLoading(false)
    }
  }

  const chooseFlight = async (flight) => {
    setLoading(true)
    setSelectedFlight(flight)

    try {
      const response = await fetch(`${API_URL}/travel/select-flight`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_request: requestPayload,
          selected_flight_id: flight.id,
          flight_options: flightOptions
        })
      })

      const data = await response.json()

      if (data.status === "no_accommodation_budget") {
        setError(data.message)
        setFlightOptions(data.flight_options)
        setStep("flights")
        return
      }

      setHouseOptions(data.house_options || [])
      setStep("houses")
    } catch (err) {
      setError("Error seleccionando vuelo")
    } finally {
      setLoading(false)
    }
  }

  const chooseHouse = async (house) => {
    setLoading(true)
    setSelectedHouse(house)

    try {
      const response = await fetch(`${API_URL}/travel/select-house`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_request: requestPayload,
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

  const handleReview = async (decision) => {
    try {
      const response = await fetch(`${API_URL}/travel/review`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          type: decision,
          comment: reviewComment,
          context: {
            user_request: requestPayload,
            selected_flight: selectedFlight,
            selected_house: selectedHouse
          }
        })
      })

      const data = await response.json()

      if (data.status === "revised" || data.status === "completed") {
        setFinalPlan(data.travel_plan)
        setStep("completed")
      }

      if (data.status === "pending_flight_selection") {
        setFlightOptions(data.flight_options)
        setSelectedFlight(null)
        setSelectedHouse(null)
        setFinalPlan(null)
        setStep("flights")
      }

      if (data.status === "pending_house_selection") {
        setHouseOptions(data.house_options)
        setSelectedHouse(null)
        setFinalPlan(null)
        setStep("houses")
      }
    } catch (err) {
      console.error("Error in review", err)
    }
  }

  return (
    <div className="container">
      <h1>🌍 Travel Planner MVP</h1>
      <StepIndicator step={step} />

      {step === "form" && (
        <div className="travel-form">
          <div className="form-row">
            <div className="form-group">
              <label>
                Origen <span className="required">*</span>
              </label>
              <input name="origin_airport" placeholder="Ej. Madrid" onChange={handleInputChange} />
            </div>
            <div className="form-group">
              <label>
                Destino <span className="required">*</span>
              </label>
              <input name="destination_country" placeholder="Ej. France" onChange={handleInputChange} />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Salida</label>
              <input type="date" name="departure_date" onChange={handleInputChange} />
            </div>
            <div className="form-group">
              <label>Regreso</label>
              <input type="date" name="return_date" onChange={handleInputChange} />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Pasajeros</label>
              <input type="number" name="passengers" placeholder="1" onChange={handleInputChange} />
            </div>
            <div className="form-group">
              <label>Presupuesto máximo (€)</label>
              <input type="number" name="max_budget" placeholder="1200" onChange={handleInputChange} />
            </div>
          </div>

          <button type="submit" onClick={startTravel} disabled={loading}>
            {loading ? "Buscando vuelos..." : "Buscar vuelos"}
          </button>
        </div>
      )}

      {step === "flights" && (
        <section>
          <h2>✈️ Selecciona un vuelo</h2>
          <p className="section-hint">Mostramos las opciones ordenadas por score multi-criterio.</p>
          <div className="cards-grid">
            {flightOptions.map((f, index) => (
              <div key={f.id} className={`card ${selectedFlight?.id === f.id ? "selected" : ""}`}>
                <div className="card-header">
                  <strong>{f.airline}</strong>
                  <span className="price">€{f.price?.toFixed(2)}</span>
                </div>
                <p>
                  {f.origin} → {f.destination}
                </p>
                <p>
                  {f.departure_date} {f.departure_time} • {f.arrival_time}
                </p>
                <ScoreBar score={f.score} />
                <p className="score-label">
                  Score total: <strong>{f.score?.toFixed?.(1) || f.score}</strong>/100
                </p>
                {index === 0 && <span className="badge best">🏆 Recomendado</span>}

                <ScoreBadges breakdown={f.scoring_breakdown} metrics={flightMetrics} />

                <button onClick={() => chooseFlight(f)} disabled={loading}>
                  {selectedFlight?.id === f.id ? "Seleccionado" : "Elegir vuelo"}
                </button>
              </div>
            ))}
          </div>
        </section>
      )}

      {step === "houses" && (
        <section>
          <h2>🏠 Selecciona alojamiento</h2>
          <p className="section-hint">Comparación multi-criterio (precio, rating, reviews, amenities).</p>
          <div className="cards-grid">
            {houseOptions.map((h, index) => (
              <div key={h.id} className={`card ${selectedHouse?.id === h.id ? "selected" : ""}`}>
                <div className="card-header">
                  <strong>{h.name}</strong>
                  <span className="price">€{h.total_price?.toFixed(2)}</span>
                </div>
                <p>
                  {h.city} · {h.type}
                </p>
                <p>
                  ⭐ {h.rating} ({h.reviews_count} reviews) • {h.max_guests} huéspedes
                </p>

                <ScoreBar score={h.score} />
                <p className="score-label">
                  Score total: <strong>{h.score?.toFixed?.(1) || h.score}</strong>/100
                </p>
                {index === 0 && <span className="badge best">🏆 Mejor relación calidad/precio</span>}

                <ScoreBadges breakdown={h.scoring_breakdown} metrics={houseMetrics} />

                {Array.isArray(h.amenities) && h.amenities.length > 0 && (
                  <div className="amenities">
                    {h.amenities.slice(0, 6).map((amenity) => (
                      <span key={amenity}>{amenity}</span>
                    ))}
                  </div>
                )}

                <button onClick={() => chooseHouse(h)} disabled={loading}>
                  {selectedHouse?.id === h.id ? "Seleccionado" : "Elegir alojamiento"}
                </button>
              </div>
            ))}
          </div>
        </section>
      )}

      {step === "completed" && (
        <section>
          <h2>📋 Plan Final</h2>

          <div className="selection-summary">
            <div>
              <h4>✈️ Vuelo</h4>
              {selectedFlight ? (
                <>
                  <p>
                    <strong>{selectedFlight.airline}</strong> · €{selectedFlight.price?.toFixed(2)}
                  </p>
                  <p>
                    {selectedFlight.origin} → {selectedFlight.destination}
                  </p>
                  <p>Score: {selectedFlight.score}/100</p>
                </>
              ) : (
                <p>No seleccionado.</p>
              )}
            </div>
            <div>
              <h4>🏠 Alojamiento</h4>
              {selectedHouse ? (
                <>
                  <p>
                    <strong>{selectedHouse.name}</strong> · €{selectedHouse.total_price?.toFixed(2)}
                  </p>
                  <p>
                    {selectedHouse.city} · {selectedHouse.type}
                  </p>
                  <p>Score: {selectedHouse.score}/100</p>
                </>
              ) : (
                <p>No seleccionado.</p>
              )}
            </div>
          </div>

          <pre className="plan-output">{finalPlan}</pre>

          <div className="review-panel">
            <h3>🧑‍⚖️ Revisión humana (HITL)</h3>
            <textarea
              placeholder="Añadir comentario o solicitar cambios..."
              value={reviewComment}
              onChange={(e) => setReviewComment(e.target.value)}
            />
            <div className="review-actions">
              <button onClick={() => handleReview("approve")}>✅ Aprobar</button>
              <button onClick={() => handleReview("editorial")}>📝 Ajustar redacción</button>
              <button onClick={() => handleReview("house_criteria")}>🏠 Cambiar alojamiento</button>
              <button onClick={() => handleReview("flight_criteria")}>✈️ Recalcular vuelos</button>
            </div>
          </div>
        </section>
      )}

      {error && <div className="error-banner">{error}</div>}
    </div>
  )
}
