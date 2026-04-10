# 🌍 Travel Planner MVP  
## Sistema Multi‑Agente de Planificación de Viajes con Human‑in‑the‑Loop (HITL)

---

## 📌 Descripción General

**Travel Planner MVP** es un sistema de planificación de viajes basado en una arquitectura multi‑agente con orquestación centralizada, motor de scoring explicable y capacidad de refinamiento iterativo mediante Human‑in‑the‑Loop (HITL).

El proyecto demuestra cómo diseñar un sistema inteligente que:

- ✅ Orquesta múltiples agentes especializados
- ✅ Implementa scoring ponderado multi‑criterio
- ✅ Permite refinamiento semántico dinámico mediante LLM
- ✅ Gestiona estados explícitos entre frontend y backend
- ✅ Mantiene separación clara de responsabilidades
- ✅ Maneja errores de presupuesto de forma controlada

El objetivo es arquitectónico y técnico: demostrar diseño modular, explicabilidad y control iterativo.

---

# 🏗 Arquitectura del Sistema

## Estilo Arquitectónico

- Arquitectura modular orientada a agentes
- Orquestación centralizada
- Backend stateless
- Flujo dirigido por estado (`status`)
- Separación clara entre:
  - Frontend (React)
  - API Backend (FastAPI)
  - Orquestador
  - Agentes especializados
  - Modelos de dominio

---

# 🔁 Flujo General del Sistema

```
Usuario
   ↓
Frontend (React)
   ↓
Backend API (FastAPI)
   ↓
TravelOrchestrator
   ↓
[FlightPlanner] → [FlightAnalyst]
                          ↓
                Selección de vuelo
                          ↓
            [HousePlanner] → [HouseAnalyst]
                          ↓
             Selección de alojamiento
                          ↓
                  [Documentalist]
                          ↓
                Plan final en Markdown
                          ↓
               Human‑in‑the‑Loop (HITL)
```

---

# 🧠 Agentes del Sistema

## ✈️ FlightPlannerAgent
Genera vuelos sintéticos (mock data en este MVP).

## 📊 FlightAnalystAgent
Rankea vuelos usando scoring ponderado:

- Precio (35%)
- Escalas (25%)
- Duración (20%)
- Alineación con presupuesto (20%)

Incluye desglose transparente por criterio.

---

## 🏠 HousePlannerAgent
Genera alojamientos sintéticos en función del presupuesto restante.

⚠️ En este MVP no hay scraping real ni APIs externas.

---

## 📈 HouseAnalystAgent
Evalúa alojamientos con scoring multi‑criterio:

- Precio (30%)
- Rating (25%)
- Reviews (15%)
- Amenities (15%)
- Alineación con presupuesto (15%)

Incluye desglose detallado por criterio.

---

## 📝 DocumentalistAgent
Genera el documento final del viaje en formato Markdown estructurado.

Permite regeneración tras revisión editorial.

---

## 🧠 Constraint Extractor (LLM)

El sistema incluye un módulo semántico basado en LLM que:

- Interpreta comentarios del usuario
- Extrae restricciones estructuradas
- Soporta español e inglés
- Devuelve JSON limpio

Ejemplo:

```
"quiero 1 baño y 2 dormitorios"
```

Se transforma en:

```
{
  "entity": "house",
  "constraints": {
    "bathrooms": 1,
    "bedrooms": 2
  }
}
```

Esto permite re‑ejecutar agentes dinámicamente.

---

# Comprobación de comunicación de agentes

<img width="660" height="205" alt="image" src="https://github.com/user-attachments/assets/aa39ec56-f0a0-46de-9918-0e0b9d6b4313" />


# 👤 Human‑in‑the‑Loop (HITL)

El sistema soporta dos modos de revisión:

## 📝 Revisar redacción
Regenera el documento final sin modificar vuelo ni alojamiento.

## 🔁 Cambiar criterios
- Interpreta semánticamente el comentario
- Reejecuta búsqueda de vuelos o alojamientos
- Devuelve nuevas opciones
- Requiere confirmación explícita del usuario

No hay selección automática oculta.

---

# 🚨 Manejo de Presupuesto Insuficiente

Si el vuelo seleccionado deja presupuesto insuficiente para alojamiento:

El backend devuelve:

```
status: "no_accommodation_budget"
```

El frontend:

- Muestra mensaje claro
- Vuelve a selección de vuelos
- Evita pantalla en blanco
- Mantiene coherencia de estado

Este diseño prioriza claridad y control del usuario.

---

# ⚙️ Stack Tecnológico

## Backend
- Python 3.10+
- FastAPI
- Pydantic
- Orquestación asíncrona
- Arquitectura modular por agentes
- Cliente LLM (Azure compatible)

## Frontend
- React
- Vite
- Fetch API
- Flujo basado en estados (`step`)
- Renderizado condicional según `status`

---

# 📊 Motor de Scoring

Características:

- Normalización relativa
- Ponderación explícita
- Transparencia total (value / max)
- Visualización gráfica
- Resaltado automático de mejor opción

Diseñado para explicabilidad.

---

# 🚀 Ejecución del Proyecto

## Backend

Desde la raíz:

```bash
uvicorn backend.api.app:app --reload
```

Disponible en:

```
http://127.0.0.1:8000
```

---

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
  agents/
  models/
  orchestrator/
  llm/
  tools/

frontend/
  src/
```

---

# ✅ Capacidades Actuales del MVP

- Flujo completo de planificación
- Arquitectura multi‑agente
- Scoring explicable
- Refinamiento semántico con LLM
- HITL real
- Manejo de presupuesto insuficiente
- Estado dirigido por backend
- Confirmación explícita tras cambios

---

# ❌ Alcance Deliberadamente Limitado

Este MVP:

- No integra APIs reales
- No realiza scraping real
- No incluye base de datos
- No incluye autenticación
- No está preparado para producción

El foco es arquitectónico.

---

# 📈 Posibles Evoluciones Futuras

- Fallback automático inteligente entre vuelos
- Persistencia con PostgreSQL
- Cache distribuida
- Versionado de planes
- Explainability avanzada
- Integración con APIs reales
- Dockerización

---

# 🎯 Principios de Diseño

- Modularidad clara
- Orquestación explícita
- Estados bien definidos
- Explicabilidad
- Control humano en decisiones
- Simplicidad antes que sobre‑ingeniería

---

# 🏁 Conclusión

Travel Planner MVP no es solo un generador de texto.

Es un sistema multi‑agente con:

- Orquestación centralizada
- Scoring ponderado
- Refinamiento semántico
- Human‑in‑the‑Loop real
- Manejo robusto de estados

Un MVP técnico sólido, coherente y extensible.

---

## 👨‍💻 Autor

Proyecto desarrollado como demostración de arquitectura multi‑agente con orquestación centralizada, motor de decisión explicable y revisión humana iterativa.
