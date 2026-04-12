# 📚 Casos de Uso  
## Travel Planner MVP – Sistema Multi‑Agente Orquestado con LangGraph

---

# 📌 Introducción

Este documento describe los casos de uso alineados con la implementación actual del sistema.

El sistema está orquestado mediante **LangGraph (StateGraph)** y utiliza un modelo de estado explícito (`TravelState`) que gobierna el flujo completo.

No existe ya un `TravelOrchestrator` manual.  
La lógica de transición entre fases se declara en el grafo.

---

# ✅ CASOS DE USO DE NEGOCIO

---

## CU‑01 – Crear Solicitud de Viaje

**Actor principal:** Usuario viajero  

### Flujo Principal

1. El usuario introduce:
   - Aeropuerto de origen
   - País de destino
   - Ciudad (opcional)
   - Fechas
   - Número de pasajeros
   - Presupuesto máximo
2. El frontend envía la solicitud al endpoint `/travel/start`.
3. El backend ejecuta el grafo desde `start`.
4. El nodo `flight` genera y rankea vuelos.
5. Estado devuelto: `pending_flight_selection`.

### Postcondición
Lista de vuelos disponible para selección explícita.

---

## CU‑02 – Seleccionar Vuelo

**Actor principal:** Usuario viajero  

### Precondición
Estado actual: `pending_flight_selection`.

### Flujo Principal

1. El usuario selecciona un vuelo.
2. Se invoca `/travel/select-flight`.
3. El grafo continúa desde `flight` → `house`.
4. Se calcula presupuesto restante.
5. Se generan y rankean alojamientos.
6. Estado devuelto:
   - `pending_house_selection`
   - o `no_accommodation_budget`.

### Flujo Alternativo – Presupuesto Insuficiente

- El nodo `house` no encuentra opciones válidas.
- Estado: `no_accommodation_budget`.
- El frontend redirige a selección de vuelos.

---

## CU‑03 – Seleccionar Alojamiento

**Actor principal:** Usuario viajero  

### Precondición
Estado actual: `pending_house_selection`.

### Flujo Principal

1. Usuario selecciona alojamiento.
2. Se invoca `/travel/select-house`.
3. El grafo ejecuta nodo `finalize`.
4. Se genera plan final en Markdown.
5. Estado devuelto: `completed`.

---

## CU‑04 – Revisar Redacción (HITL Editorial)

**Actor principal:** Usuario viajero  

### Precondición
Estado actual: `completed`.

### Flujo Principal

1. Usuario envía comentario editorial.
2. Se invoca `/travel/review`.
3. El nodo `review` enruta a `finalize`.
4. Se regenera el documento.
5. Estado devuelto: `completed` (plan actualizado).

---

## CU‑05 – Cambiar Criterios (HITL Semántico)

**Actor principal:** Usuario viajero  

### Precondición
Estado actual: `completed`.

### Flujo Principal

1. Usuario introduce comentario en lenguaje natural.
2. Se invoca `/travel/review`.
3. El grafo enruta según `review_type`:
   - `house_criteria` → nodo `house`
   - `flight_criteria` / `criteria` → nodo `flight`
4. El LLM extrae restricciones estructuradas.
5. Se re‑ejecuta la fase correspondiente.
6. Estado devuelto:
   - `pending_house_selection`
   - `pending_flight_selection`
   - o `error`.

No se realizan selecciones automáticas.

---

# 🧠 Procesos Internos Relevantes

## PI‑01 – Orquestación Declarativa

El flujo del sistema está definido mediante:

```python
builder.add_edge(...)
builder.add_conditional_edges(...)
```

No existe lógica imperativa secuencial externa.

---

## PI‑02 – Gestión de Estados

Estados soportados:

- `pending_flight_selection`
- `pending_house_selection`
- `completed`
- `no_accommodation_budget`
- `error`

El frontend renderiza en función del `status`.

---

## PI‑03 – Extracción Semántica

El módulo LLM:

- Interpreta texto libre
- Devuelve JSON estructurado
- Permite filtrado dinámico
- Soporta español e inglés

---

# 🚫 Funcionalidades No Implementadas

- Persistencia de sesiones
- Versionado de planes
- Iteraciones automáticas Generador ↔ Crítico
- Infraestructura distribuida
- Gestión multiusuario

---

# ✅ Conclusión

Los casos de uso reflejan fielmente el sistema actual:

- Orquestación mediante LangGraph
- Flujo dirigido por estado
- Selección explícita del usuario
- HITL real
- Integración controlada de LLM
