# 🌍 Travel Planner MVP  
## Sistema Multi‑Agente con Orquestación basada en LangGraph y HITL

---

## 📌 Descripción General

**Travel Planner MVP** es un sistema de planificación de viajes basado en una arquitectura multi‑agente orquestada mediante **LangGraph (StateGraph)**, con motor de scoring explicable y refinamiento iterativo controlado por Human‑in‑the‑Loop (HITL).

El objetivo del proyecto es demostrar:

- ✅ Orquestación declarativa mediante grafo de estados
- ✅ Separación clara entre API, grafo, nodos y dominio
- ✅ Scoring multi‑criterio explicable
- ✅ Integración controlada de LLM para extracción semántica
- ✅ Control explícito del flujo mediante estados
- ✅ Intervención humana real en decisiones críticas

---

# 🏗 Arquitectura del Sistema

## Estilo Arquitectónico

- Arquitectura modular orientada a agentes
- Orquestación declarativa con **LangGraph**
- Backend stateless
- Flujo dirigido por estado (`TravelState`)
- Separación clara entre:
  - Frontend (React + Vite)
  - API (FastAPI)
  - Grafo (LangGraph StateGraph)
  - Nodos
  - Dominio
  - Cliente LLM

---

# 🔁 Orquestación con LangGraph

El sistema utiliza:

```python
StateGraph(TravelState)
```

## Nodos del grafo

- `start`
- `flight`
- `house`
- `finalize`
- `review`
- `error`

## Flujo principal

```
start → flight → house → finalize → END
```

## Flujo HITL condicional

El nodo `review` enruta dinámicamente según:

- `editorial` → finalize
- `house_criteria` → house
- `flight_criteria` / `criteria` → flight

La decisión se toma mediante `add_conditional_edges()`.

---

# 🧠 TravelState

El estado compartido del grafo contiene:

- user_request
- flight_options
- selected_flight
- house_options
- selected_house
- travel_plan
- status
- review_type
- review_comment
- error_message

El backend es stateless: el estado vive únicamente durante la ejecución del grafo.

---

# 🧠 Agentes del Sistema

## ✈️ FlightPlanner + FlightAnalyst
- Generación de vuelos sintéticos
- Ranking con scoring ponderado:
  - Precio (35%)
  - Escalas (25%)
  - Duración (20%)
  - Presupuesto (20%)

## 🏠 HousePlanner + HouseAnalyst
- Generación de alojamientos sintéticos
- Scoring multi‑criterio:
  - Precio (30%)
  - Rating (25%)
  - Reviews (15%)
  - Amenities (15%)
  - Presupuesto (15%)

## 📝 Documentalist
Genera el plan final en Markdown estructurado.

## 🧠 Constraint Extractor (LLM)
Interpreta lenguaje natural y devuelve JSON estructurado para:

- bathrooms
- bedrooms
- beds
- max_guests

---

# 👤 Human‑in‑the‑Loop (HITL)

El sistema soporta:

## 📝 Revisión editorial
- Regenera únicamente el documento final.
- No altera vuelo ni alojamiento.

## 🔁 Cambio de criterios
- Extrae restricciones con LLM.
- Re‑ejecuta nodos del grafo.
- Devuelve nuevas opciones.
- Requiere confirmación explícita.

No existe selección automática sin intervención del usuario.

---

# 🚨 Manejo de Presupuesto Insuficiente

Si no existen alojamientos dentro del presupuesto restante:

```
status: "no_accommodation_budget"
```

El frontend:
- Muestra mensaje claro
- Vuelve a selección de vuelos
- Mantiene coherencia de estado

---

# ⚙️ Stack Tecnológico

## Backend
- Python 3.10+
- FastAPI
- LangGraph
- Pydantic
- Cliente LLM (Azure compatible)
- Arquitectura async

## Frontend
- React
- Vite
- Fetch API
- Renderizado basado en `status`

---

# 📊 Motor de Scoring

Características:

- Normalización relativa
- Ponderación explícita
- Desglose transparente
- Explicabilidad priorizada

---

# 🚀 Ejecución

## Backend

```bash
uvicorn backend.api.app:app --reload
```

Disponible en:
```
http://127.0.0.1:8000
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Disponible en:
```
http://localhost:5173
```

---

# 📁 Estructura del Proyecto

```
backend/
  api/
  graph/
  domain/
  models/
  llm/
  tools/

frontend/
  src/
```

---

# Comprobación de comunicación de agentes

<img width="660" height="205" alt="image" src="https://github.com/user-attachments/assets/aa39ec56-f0a0-46de-9918-0e0b9d6b4313" />

---

# ✅ Capacidades del MVP

- Orquestación declarativa con LangGraph
- Flujo multi‑agente controlado por estado
- HITL real
- Scoring explicable
- Interpretación semántica con LLM
- Manejo robusto de errores
- Backend stateless

---

# 🚫 Limitaciones

- No APIs reales
- No scraping real
- No base de datos
- No autenticación
- No preparado para producción

---

# 🎯 Principios de Diseño

- Orquestación explícita
- Estado bien definido
- Control humano en decisiones
- Modularidad
- Simplicidad sobre sobre‑ingeniería

---

## 👨‍💻 Autor

Proyecto desarrollado como demostración arquitectónica de un sistema multi‑agente orquestado mediante LangGraph con refinamiento iterativo controlado.
