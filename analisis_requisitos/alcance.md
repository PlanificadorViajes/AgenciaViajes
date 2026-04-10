# 🌍 Travel Planner MVP – Alcance del Sistema  
## Sistema Multi‑Agente con Orquestación Centralizada y Human‑in‑the‑Loop

---

# 1️⃣ Alcance Funcional del MVP

## ✅ Funcionalidades Incluidas

El MVP actual implementa un sistema completo de planificación de viajes con arquitectura multi‑agente y control iterativo mediante intervención humana.

### 📌 Entrada de Usuario

El sistema permite crear una solicitud de viaje con:

- Aeropuerto de origen
- País de destino
- Ciudad opcional
- Fechas (ida y vuelta)
- Número de pasajeros
- Presupuesto máximo

---

### ✈️ Fase 1 – Búsqueda y Selección de Vuelo

- Generación de vuelos sintéticos.
- Evaluación automática mediante scoring ponderado.
- Visualización transparente del desglose de puntuación.
- Selección explícita por parte del usuario.

---

### 🏠 Fase 2 – Búsqueda y Selección de Alojamiento

- Cálculo automático del presupuesto restante.
- Generación de alojamientos sintéticos.
- Evaluación mediante scoring multi‑criterio.
- Selección explícita por parte del usuario.
- Manejo de caso especial:
  - Si no hay alojamiento dentro del presupuesto → el sistema informa y redirige a selección de vuelo.

---

### 📝 Fase 3 – Generación de Plan Final

- Generación de documento final en formato Markdown.
- Inclusión de:
  - Vuelo seleccionado
  - Alojamiento seleccionado
  - Alternativas
  - Desglose presupuestario
  - Pasos siguientes

---

### 👤 Human‑in‑the‑Loop (HITL)

El sistema soporta dos modos de revisión:

#### 📝 Revisión editorial
- Regenera únicamente el documento final.
- No altera vuelo ni alojamiento.

#### 🔁 Cambio de criterios (semántico)
- Interpreta comentario del usuario mediante LLM.
- Extrae restricciones estructuradas.
- Re‑ejecuta búsqueda de vuelos o alojamientos.
- Devuelve nuevas opciones para confirmación explícita.
- Nunca selecciona automáticamente sin intervención humana.

---

### 🧠 Extracción Semántica de Restricciones

El sistema incorpora un módulo LLM que:

- Interpreta comentarios en español o inglés.
- Extrae:
  - bathrooms
  - bedrooms
  - beds
  - max_guests
- Devuelve JSON estructurado.
- Permite filtrado dinámico sin reglas hardcodeadas.

---

## 🔄 Flujo End‑to‑End Cubierto

1. Usuario crea solicitud.
2. Generación y ranking de vuelos.
3. Selección explícita de vuelo.
4. Generación y ranking de alojamientos.
5. Selección explícita de alojamiento.
6. Generación del plan final.
7. Revisión HITL opcional.
8. Regeneración o filtrado según feedback.

---

## 👥 Actores del Sistema

- Usuario viajero
- Frontend React
- Backend FastAPI
- TravelOrchestrator
- FlightPlannerAgent
- FlightAnalystAgent
- HousePlannerAgent
- HouseAnalystAgent
- DocumentalistAgent
- Módulo LLM (Constraint Extractor)

---

## 🚫 Fuera de Alcance

El MVP **NO incluye**:

- Integraciones reales con APIs externas.
- Scraping real.
- Persistencia en base de datos.
- Autenticación o multiusuario.
- Optimización matemática avanzada.
- Gestión concurrente avanzada.
- Infraestructura distribuida.

El sistema opera en modo sintético (mock data).

---

# 2️⃣ Alcance Técnico

## 🏗 Arquitectura

- Arquitectura modular monolítica.
- Orquestación centralizada mediante clase `TravelOrchestrator`.
- Backend stateless.
- Flujo dirigido por estados (`status`).
- Comunicación frontend ↔ backend vía REST.

---

## 🧩 Componentes Principales

- API Layer (FastAPI)
- TravelOrchestrator
- Agentes especializados:
  - FlightPlanner
  - FlightAnalyst
  - HousePlanner
  - HouseAnalyst
  - Documentalist
- Cliente LLM (Azure compatible)
- Frontend React basado en estados (`step`)

---

## 🔁 Orquestación

La lógica de flujo depende del `status` devuelto por backend:

- `pending_flight_selection`
- `pending_house_selection`
- `completed`
- `revised`
- `no_accommodation_budget`
- `error`

El frontend reacciona explícitamente a cada estado.

---

## 🧠 Gestión de Estado

El backend es stateless.

El frontend mantiene:

- step
- selectedFlight
- selectedHouse
- finalPlan
- flightOptions
- houseOptions

No existe persistencia entre reinicios.

---

## ⚠️ Manejo de Errores

Incluye:

- Manejo de excepciones en orquestador.
- Logging estructurado.
- Estado explícito para presupuesto insuficiente.
- Mensaje claro al usuario.

No incluye:

- Retries automáticos.
- Circuit breakers.
- Clasificación avanzada de errores.

---

## 💾 Persistencia

El MVP no implementa persistencia estructurada.

- No hay base de datos.
- No se almacenan sesiones.
- No hay versionado histórico.

---

# 3️⃣ Objetivos del Sistema

## 🎯 Estratégicos

- Validar arquitectura multi‑agente modular.
- Demostrar integración controlada de LLM.
- Implementar HITL real y gobernanza explícita.
- Mostrar diseño orientado a estado robusto.

---

## ⚙️ Operativos

- Garantizar coherencia entre frontend y backend.
- Asegurar selección explícita en cada fase.
- Manejar correctamente presupuestos insuficientes.
- Permitir refinamiento semántico sin romper flujo.

---

# 4️⃣ Límites del Sistema

## 🔒 Funcionales

- No garantiza precios reales.
- No valida disponibilidad real.
- No realiza reservas reales.

---

## 🧱 Técnicos

- Memoria volátil.
- Sin paralelización.
- Dependencia directa del LLM para interpretación semántica.
- Sin infraestructura de producción.

---

# 5️⃣ Supuestos Clave

## 🧪 Técnicos

- El LLM devuelve JSON correctamente formateado.
- Los modelos Pydantic mantienen coherencia estructural.
- El frontend respeta el contrato de estados.

---

## 👤 De Usuario

- El usuario proporciona datos válidos.
- El usuario confirma explícitamente tras cambios.

---

## 🖥️ Infraestructura

- Sistema mono‑instancia.
- Uso académico / demostrativo.
- Baja concurrencia.

---

# 6️⃣ Riesgos Identificados

## 🛠 Técnicos

- Inconsistencia en respuestas del LLM.
- Cambios de contrato entre frontend y backend.
- Falta de persistencia ante reinicio.

---

## 📉 Experiencia de Usuario

- Presupuesto insuficiente frecuente.
- Falta de datos reales.
- Latencia acumulada por re‑ejecuciones.

---

## 📈 Escalabilidad

- No preparado para múltiples sesiones concurrentes.
- Sin separación de workers.
- Sin cache.

---

# 7️⃣ Métricas de Éxito (KPIs del MVP)

- Flujo completo sin errores.
- Re‑ejecución correcta tras cambio de criterios.
- Consistencia del estado frontend.
- Manejo correcto de presupuesto insuficiente.
- Coherencia estructural del output final.

---

# ✅ Conclusión

El MVP actual implementa correctamente:

- Arquitectura multi‑agente modular.
- Orquestación centralizada.
- Scoring explicable.
- Refinamiento semántico con LLM.
- Human‑in‑the‑Loop real.
- Manejo robusto de estados y presupuesto.

El sistema está bien delimitado como experimento técnico arquitectónico y constituye una base sólida para futuras extensiones.
