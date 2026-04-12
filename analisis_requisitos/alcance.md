# 🌍 Travel Planner MVP – Alcance del Sistema  
## Sistema Multi‑Agente Orquestado con LangGraph y Human‑in‑the‑Loop

---

# 1️⃣ Alcance Funcional del MVP

El sistema implementa un flujo completo de planificación de viajes mediante una arquitectura multi‑agente orquestada con **LangGraph (StateGraph)**.

---

## ✅ Funcionalidades Incluidas

### 📌 Entrada de Usuario

El sistema permite crear una solicitud de viaje con:

- Aeropuerto de origen
- País de destino
- Ciudad opcional
- Fechas (ida y vuelta)
- Número de pasajeros
- Presupuesto máximo

La solicitud activa el grafo desde el nodo `start`.

---

### ✈️ Fase 1 – Búsqueda y Selección de Vuelo

- Generación de vuelos sintéticos.
- Evaluación automática mediante scoring ponderado.
- Visualización transparente del desglose de puntuación.
- Selección explícita por parte del usuario.
- Estado devuelto: `pending_flight_selection`.

---

### 🏠 Fase 2 – Búsqueda y Selección de Alojamiento

- Cálculo automático del presupuesto restante.
- Generación de alojamientos sintéticos.
- Evaluación mediante scoring multi‑criterio.
- Selección explícita del usuario.
- Estados posibles:
  - `pending_house_selection`
  - `no_accommodation_budget`

---

### 📝 Fase 3 – Generación de Plan Final

- Generación de documento final en formato Markdown.
- Inclusión de:
  - Vuelo seleccionado
  - Alojamiento seleccionado
  - Desglose presupuestario
  - Información relevante estructurada
- Estado devuelto: `completed`.

---

### 👤 Human‑in‑the‑Loop (HITL)

El sistema soporta dos modos:

#### 📝 Revisión editorial
- Regenera el documento final.
- No altera vuelo ni alojamiento.

#### 🔁 Cambio de criterios (semántico)
- Interpreta comentario mediante LLM.
- Extrae restricciones estructuradas.
- Re‑ejecuta nodo correspondiente del grafo.
- Devuelve nuevas opciones para confirmación explícita.

No existen decisiones automáticas finales sin intervención humana.

---

## 🔄 Flujo End‑to‑End Cubierto

1. Usuario crea solicitud.
2. Nodo `flight` genera y rankea vuelos.
3. Usuario selecciona vuelo.
4. Nodo `house` genera y rankea alojamientos.
5. Usuario selecciona alojamiento.
6. Nodo `finalize` genera plan final.
7. Usuario puede revisar mediante nodo `review`.

Todo el flujo está gobernado por `TravelState`.

---

## 👥 Actores del Sistema

- Usuario viajero
- Frontend React
- Backend FastAPI
- LangGraph (motor de orquestación)
- Nodos del grafo
- Módulo LLM

---

## 🚫 Fuera de Alcance

El MVP NO incluye:

- APIs reales de vuelos o alojamientos
- Scraping real
- Persistencia en base de datos
- Autenticación
- Multiusuario
- Infraestructura distribuida
- Entorno productivo

El sistema opera con datos sintéticos.

---

# 2️⃣ Alcance Técnico

---

## 🏗 Arquitectura

- Arquitectura modular monolítica.
- Orquestación declarativa mediante `StateGraph`.
- Backend stateless.
- Flujo dirigido por estado explícito.
- Comunicación frontend ↔ backend vía REST.

---

## 🧩 Componentes Principales

- FastAPI (API Layer)
- LangGraph (Orquestación)
- Nodos del grafo
- Módulos de dominio
- Cliente LLM
- Frontend React

---

## 🔁 Orquestación

El flujo se define mediante:

```python
builder.add_edge(...)
builder.add_conditional_edges(...)
```

No existe secuencia imperativa externa.

---

## 🧠 Gestión de Estado

El estado se define mediante `TravelState`.

El backend no mantiene sesiones persistentes.

El frontend mantiene estado temporal para renderizado.

---

## ⚠️ Manejo de Errores

Incluye:

- Estado `error`
- Estado `no_accommodation_budget`
- Logging básico
- Manejo de excepciones en nodos

No incluye:

- Retries automáticos
- Circuit breakers
- Observabilidad avanzada

---

## 💾 Persistencia

No hay base de datos.
No se almacenan sesiones.
No hay versionado histórico.

---

# 3️⃣ Objetivos del Sistema

---

## 🎯 Estratégicos

- Validar arquitectura multi‑agente orquestada con LangGraph.
- Demostrar integración controlada de LLM.
- Implementar HITL real.
- Diseñar sistema basado en estado explícito.

---

## ⚙️ Operativos

- Garantizar coherencia entre frontend y backend.
- Mantener selección explícita en cada fase.
- Manejar correctamente presupuesto insuficiente.
- Permitir refinamiento semántico sin romper flujo.

---

# 4️⃣ Límites del Sistema

---

## 🔒 Funcionales

- No garantiza precios reales.
- No valida disponibilidad real.
- No realiza reservas.

---

## 🧱 Técnicos

- Memoria volátil.
- Sin paralelización avanzada.
- Dependencia del LLM para interpretación semántica.
- No preparado para alta concurrencia.

---

# 5️⃣ Supuestos Clave

---

## 🧪 Técnicos

- El LLM devuelve JSON válido.
- El frontend respeta el contrato de estados.
- Los modelos mantienen coherencia estructural.

---

## 👤 De Usuario

- El usuario introduce datos válidos.
- Confirma explícitamente tras cambios.

---

# 6️⃣ Riesgos Identificados

---

## 🛠 Técnicos

- Inconsistencia en respuestas del LLM.
- Cambios de contrato entre frontend y backend.
- Falta de persistencia ante reinicio.

---

## 📉 Experiencia de Usuario

- Presupuesto insuficiente frecuente.
- Datos no reales.
- Latencia acumulada por re‑ejecuciones.

---

## 📈 Escalabilidad

- No preparado para múltiples sesiones concurrentes.
- Sin cache.
- Sin separación de workers.

---

# ✅ Conclusión

El MVP implementa:

- Orquestación declarativa con LangGraph.
- Flujo multi‑agente modular.
- HITL real.
- Scoring explicable.
- Estado explícito y controlado.

El sistema está bien delimitado como demostración arquitectónica y constituye una base sólida para evolución futura.
