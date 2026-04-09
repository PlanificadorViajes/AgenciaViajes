# 🌍 Travel Planner MVP  
## Sistema Multi‑Agente de Planificación de Viajes con Human‑in‑the‑Loop

---

## 📌 Descripción General

**Travel Planner MVP** es un sistema modular de planificación de viajes basado en una arquitectura multi‑agente con orquestación centralizada y capacidad de revisión humana iterativa (Human‑in‑the‑Loop).

El objetivo del proyecto es demostrar, a nivel técnico y arquitectónico, cómo diseñar un sistema inteligente que:

- ✅ Utiliza múltiples agentes especializados  
- ✅ Implementa un motor de scoring ponderado multi‑criterio  
- ✅ Explica de forma transparente sus recomendaciones  
- ✅ Permite refinamiento iterativo mediante intervención humana  
- ✅ Mantiene una separación clara de responsabilidades  

Este proyecto está concebido como un **MVP técnico sólido**, priorizando arquitectura, explicabilidad y diseño modular por encima de integraciones externas complejas.

---

# 🏗 Arquitectura del Sistema

## Estilo Arquitectónico

- Arquitectura modular orientada a agentes
- Orquestación centralizada
- Separación clara entre:
  - Capa de Presentación (Frontend)
  - API Backend
  - Lógica Multi‑Agente
  - Modelos de Dominio

---

## 🔁 Flujo General del Sistema

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
Genera opciones de vuelos (datos sintéticos en el MVP).

## 📊 FlightAnalystAgent
Evalúa y rankea vuelos mediante un sistema de scoring ponderado:

- Precio (35%)
- Número de escalas (25%)
- Duración (20%)
- Alineación con presupuesto (20%)

Incluye desglose detallado con valores máximos:

Ejemplo:

```
Precio: 18.4 / 35
Escalas: 25 / 25
Duración: 15 / 20
Presupuesto: 12 / 20
Total: 70.4 / 100
```

---

## 🏠 HousePlannerAgent
Genera opciones de alojamiento en función del presupuesto restante.

## 📈 HouseAnalystAgent
Evalúa alojamientos con scoring multi‑criterio:

- Precio (30%)
- Rating (25%)
- Número de reviews (15%)
- Amenities (15%)
- Alineación con presupuesto (15%)

También incluye desglose transparente y valores máximos.

---

## 📝 DocumentalistAgent
Genera el documento final del viaje en formato Markdown estructurado.

Permite regeneración del plan cuando se activa el modo de revisión humana.

---

# 👤 Human‑in‑the‑Loop (HITL)

El sistema incorpora revisión humana con dos modos explícitos:

## 📝 Revisar redacción
- Regenera el documento teniendo en cuenta el comentario del usuario.
- No modifica vuelos ni alojamientos seleccionados.

## 🔁 Cambiar criterios
- Reinicia el flujo desde la búsqueda de vuelos.
- Reejecuta agentes manteniendo la solicitud original del usuario.
- Permite iteración controlada sin sobre‑ingeniería.

Este enfoque mantiene el MVP limpio y arquitectónicamente coherente.

---

# ⚙️ Stack Tecnológico

## Backend
- Python 3.10+
- FastAPI
- Pydantic
- Orquestación asíncrona
- Diseño modular por agentes

## Frontend
- React
- Vite
- Fetch API
- Flujo por estados (step‑based UI)

---

# 📊 Motor de Scoring

Características principales:

- Normalización relativa de valores
- Ponderación explícita por criterio
- Transparencia total (value / max)
- Visualización mediante barra proporcional
- Resaltado automático de la mejor opción

Este diseño prioriza explicabilidad y confianza del usuario.

---

# 🚀 Ejecución del Proyecto

## 1️⃣ Backend

Desde la raíz del proyecto:

```bash
uvicorn backend.api.app:app --reload
```

Disponible en:

```
http://127.0.0.1:8000
```

---

## 2️⃣ Frontend

```bash
cd frontend
npm install
npm start
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

- Flujo completo de planificación de viaje
- Sistema multi‑agente funcional
- Ranking ponderado multi‑criterio
- Desglose explicable de recomendaciones
- Visualización clara en frontend
- Iteración mediante HITL
- Backend stateless (sin base de datos)

---

# ❌ Alcance Deliberadamente Limitado (MVP)

Para mantener el enfoque arquitectónico:

- No integra APIs reales de vuelos
- No incluye scraping real
- No utiliza base de datos
- No incorpora autenticación
- No implementa caché distribuida
- No está preparado para producción

Estas extensiones quedan abiertas para futuras iteraciones.

---

# 🎯 Principios de Diseño

- Simplicidad antes que sobre‑ingeniería
- Explicabilidad antes que caja negra
- Modularidad clara
- Orquestación explícita
- Iteración controlada con intervención humana

---

# 📈 Posibles Evoluciones Futuras

- Persistencia con PostgreSQL
- Caché con Redis
- Integración con APIs reales
- Versionado de planes
- Optimización avanzada de costes
- Despliegue en contenedores Docker

---

# 🏁 Conclusión

Travel Planner MVP demuestra cómo diseñar un sistema multi‑agente explicable, modular y refinable mediante intervención humana.

No es simplemente un generador de texto, sino un motor de decisión con:

- Orquestación estructurada  
- Scoring transparente  
- Iteración controlada  
- Separación clara de responsabilidades  

Se trata de un MVP técnico sólido, defendible y extensible.

---

## 👨‍💻 Autor

Proyecto desarrollado como demostración de arquitectura multi‑agente con orquestación centralizada y revisión humana iterativa.
