import { useState } from "react"

export default function App() {
  const [formData, setFormData] = useState({
    origin_airport: "",
    destination_country: "",
    departure_date: "",
    return_date: "",
    passengers: "",
    budget: ""
  })
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [validationErrors, setValidationErrors] = useState({})

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
    // Clear validation error for this field when user starts typing
    if (validationErrors[name]) {
      setValidationErrors(prev => ({
        ...prev,
        [name]: ""
      }))
    }
  }

  const validateForm = () => {
    const errors = {}

    if (!formData.origin_airport.trim()) {
      errors.origin_airport = "El aeropuerto de origen es obligatorio"
    }

    if (!formData.destination_country.trim()) {
      errors.destination_country = "El país destino es obligatorio"
    }

    if (!formData.departure_date) {
      errors.departure_date = "La fecha de ida es obligatoria"
    }

    if (!formData.return_date) {
      errors.return_date = "La fecha de vuelta es obligatoria"
    }

    if (formData.departure_date && formData.return_date) {
      const departureDate = new Date(formData.departure_date)
      const returnDate = new Date(formData.return_date)
      if (returnDate <= departureDate) {
        errors.return_date = "La fecha de vuelta debe ser posterior a la fecha de ida"
      }
    }

    if (!formData.passengers) {
      errors.passengers = "El número de pasajeros es obligatorio"
    } else if (parseInt(formData.passengers) < 1) {
      errors.passengers = "Debe haber al menos 1 pasajero"
    } else if (parseInt(formData.passengers) > 10) {
      errors.passengers = "Máximo 10 pasajeros"
    }

    if (!formData.budget) {
      errors.budget = "El presupuesto es obligatorio"
    } else if (parseFloat(formData.budget) < 0) {
      errors.budget = "El presupuesto debe ser un valor positivo"
    }

    setValidationErrors(errors)
    return Object.keys(errors).length === 0
  }

  const generatePlan = async () => {
    if (!validateForm()) {
      setError("Por favor, completa todos los campos obligatorios correctamente")
      return
    }

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
          origin_airport: formData.origin_airport,
          destination_country: formData.destination_country,
          departure_date: formData.departure_date,
          return_date: formData.return_date,
          passengers: parseInt(formData.passengers),
          budget: parseFloat(formData.budget)
        })
      })

      if (!response.ok) {
        throw new Error("API error")
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError("Error al generar el itinerario. Por favor, intenta de nuevo.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <h1>🌍 Travel Itinerary Generator</h1>

      <form className="travel-form" onSubmit={(e) => { e.preventDefault(); generatePlan(); }}>
        <div className="form-group">
          <label htmlFor="origin_airport">
            Aeropuerto de Origen <span className="required">*</span>
          </label>
          <input
            type="text"
            id="origin_airport"
            name="origin_airport"
            placeholder="ej: MAD, BCN, AGP..."
            value={formData.origin_airport}
            onChange={handleInputChange}
            className={validationErrors.origin_airport ? "error" : ""}
          />
          {validationErrors.origin_airport && (
            <span className="error-message">{validationErrors.origin_airport}</span>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="destination_country">
            País Destino <span className="required">*</span>
          </label>
          <input
            type="text"
            id="destination_country"
            name="destination_country"
            placeholder="ej: Francia, Japón, Italia..."
            value={formData.destination_country}
            onChange={handleInputChange}
            className={validationErrors.destination_country ? "error" : ""}
          />
          {validationErrors.destination_country && (
            <span className="error-message">{validationErrors.destination_country}</span>
          )}
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="departure_date">
              Fecha de Ida <span className="required">*</span>
            </label>
            <input
              type="date"
              id="departure_date"
              name="departure_date"
              value={formData.departure_date}
              onChange={handleInputChange}
              min={new Date().toISOString().split('T')[0]}
              className={validationErrors.departure_date ? "error" : ""}
            />
            {validationErrors.departure_date && (
              <span className="error-message">{validationErrors.departure_date}</span>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="return_date">
              Fecha de Vuelta <span className="required">*</span>
            </label>
            <input
              type="date"
              id="return_date"
              name="return_date"
              value={formData.return_date}
              onChange={handleInputChange}
              min={formData.departure_date || new Date().toISOString().split('T')[0]}
              className={validationErrors.return_date ? "error" : ""}
            />
            {validationErrors.return_date && (
              <span className="error-message">{validationErrors.return_date}</span>
            )}
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="passengers">
              Número de Pasajeros <span className="required">*</span>
            </label>
            <input
              type="number"
              id="passengers"
              name="passengers"
              placeholder="1"
              min="1"
              max="10"
              value={formData.passengers}
              onChange={handleInputChange}
              className={validationErrors.passengers ? "error" : ""}
            />
            {validationErrors.passengers && (
              <span className="error-message">{validationErrors.passengers}</span>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="budget">
              Presupuesto (€) <span className="required">*</span>
            </label>
            <input
              type="number"
              id="budget"
              name="budget"
              placeholder="1000"
              min="0"
              step="0.01"
              value={formData.budget}
              onChange={handleInputChange}
              className={validationErrors.budget ? "error" : ""}
            />
            {validationErrors.budget && (
              <span className="error-message">{validationErrors.budget}</span>
            )}
          </div>
        </div>

        <button type="submit" disabled={loading}>
          {loading ? "Generando..." : "Generar Plan de Viaje"}
        </button>
      </form>

      {error && <p className="error-banner">{error}</p>}

      {result && (
        <div className="result">
          <h2>📋 Plan de Viaje Generado</h2>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  )
}
