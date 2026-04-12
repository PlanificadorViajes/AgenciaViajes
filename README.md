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
  - Tools
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

Aunque la ejecución está orquestada por nodos del grafo, conceptualmente el sistema sigue un modelo multi‑agente donde cada fase encapsula una responsabilidad clara.

---

## ✈️ FlightPlannerAgent

Responsabilidad:
- Generar propuestas de vuelos (mock en este MVP).
- Construir opciones estructuradas compatibles con el dominio.

Características:
- No realiza llamadas a APIs reales.
- Produce datos normalizados.
- Prepara la base para evaluación posterior.

---

## 📊 FlightAnalystAgent

Responsabilidad:
- Evaluar y rankear vuelos mediante scoring ponderado.

Criterios utilizados:
- Precio (35%)
- Escalas (25%)
- Duración (20%)
- Alineación con presupuesto (20%)

Características:
- Normalización relativa.
- Desglose transparente por criterio.
- Resultado explicable y reproducible.

---

## 🏠 HousePlannerAgent

Responsabilidad:
- Generar alojamientos compatibles con el presupuesto restante.
- Aplicar restricciones semánticas si existen (HITL).

Características:
- Usa información del vuelo seleccionado.
- Puede re‑ejecutarse dinámicamente tras revisión.

---

## 📈 HouseAnalystAgent

Responsabilidad:
- Evaluar alojamientos mediante scoring multi‑criterio.

Criterios utilizados:
- Precio (30%)
- Rating (25%)
- Reviews (15%)
- Amenities (15%)
- Alineación con presupuesto (15%)

Características:
- Transparencia total del cálculo.
- Ranking determinista.
- Explicabilidad priorizada.

---

## 📝 DocumentalistAgent

Responsabilidad:
- Generar el plan final estructurado en Markdown.
- Integrar vuelo, alojamiento y contexto del usuario.

Características:
- Salida coherente y estructurada.
- Puede regenerarse tras revisión editorial.
- No altera decisiones seleccionadas.

---

## 🧠 Constraint Extractor (LLM)

Responsabilidad:
- Interpretar lenguaje natural del usuario.
- Extraer restricciones estructuradas en JSON.

Reconoce:
- bathrooms
- bedrooms
- beds
- max_guests

Características:
- Soporte en español e inglés.
- Devuelve estructura limpia para re‑ejecución del grafo.
- No toma decisiones finales automáticamente.

---

# 🛠 Tools Utilizadas

Las herramientas encapsulan lógica ejecutable reutilizable y separan el grafo del dominio.

## 🔎 search_flights_tool
- Genera vuelos sintéticos.
- Devuelve lista estructurada compatible con el dominio.
- Usada por el nodo `flight`.

## 🏠 search_accommodations_tool
- Genera alojamientos sintéticos.
- Considera presupuesto restante tras selección de vuelo.
- Usada por el nodo `house`.

## 📝 generate_travel_plan_tool
- Construye el documento final en Markdown.
- Integra información del usuario, vuelo y alojamiento.
- Usada por el nodo `finalize`.

## 🌐 web_scraper (estructura preparada)
- Actualmente no activo en producción.
- Preparado para futura integración con fuentes externas.

Las tools permiten:
- Separación de responsabilidades.
- Sustitución futura por integraciones reales.
- Testeo independiente del grafo.
## Comuniación inical (usuario mete los datos necesarios)

<img width="665" height="121" alt="image" src="https://github.com/user-attachments/assets/386cdfa9-4c57-4607-9ada-53a2ddb78505" />

## Comunicación al elegir el vuelo:

<img width="656" height="168" alt="image" src="https://github.com/user-attachments/assets/985d88ea-2545-4848-b773-3549a8c09616" />

## Comunicación al elegir el vuelo:

<img width="672" height="115" alt="image" src="https://github.com/user-attachments/assets/732d7f44-d6a6-4e8d-a70f-29598fdbc6ed" />

## Comnicación tras la solucitud del HITL:

<img width="673" height="444" alt="image" src="https://github.com/user-attachments/assets/afeffe40-1069-47e4-a86e-66a745134736" />

(selecciona el agente necesario y vuelve a elegir el usuario)

## Devolución final teniendo en cuenta lo solicitado del HITL:

<img width="683" height="102" alt="image" src="https://github.com/user-attachments/assets/f32bbfff-7ae2-4471-83bb-3c9d3d6aadd0" />



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
- Ranking determinista

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



# ✅ Capacidades del MVP

- Orquestación declarativa con LangGraph
- Flujo multi‑agente controlado por estado
- HITL real
- Scoring explicable
- Interpretación semántica con LLM
- Manejo robusto de errores
- Backend stateless
- Separación clara entre grafo, dominio y tools

---

# 🚫 Limitaciones

- No APIs reales
- No scraping real activo
- No base de datos
- No autenticación
- No preparado para producción

---

# 🎯 Principios de Diseño

- Orquestación explícita
- Estado bien definido
- Control humano en decisiones
- Modularidad
- Explicabilidad
- Simplicidad sobre sobre‑ingeniería

---

## 👨‍💻 Autor

Proyecto desarrollado como demostración arquitectónica de un sistema multi‑agente orquestado mediante LangGraph con refinamiento iterativo controlado.
