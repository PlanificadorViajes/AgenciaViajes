# 📘 Historias de Usuario – Travel Planner MVP  
## Sistema Multi‑Agente Orquestado con LangGraph y HITL

---

# 🧭 Épica 1 – Planificación de Viaje

---

## HU‑01 – Crear Solicitud de Viaje

**Como** usuario viajero  
**Quiero** introducir los datos básicos de mi viaje  
**Para** obtener propuestas de vuelos acordes a mis preferencias.

### Criterios de aceptación

- El sistema solicita:
  - Aeropuerto de origen
  - País de destino
  - Ciudad opcional
  - Fechas
  - Número de pasajeros
  - Presupuesto máximo
- El frontend invoca `/travel/start`.
- El backend ejecuta el grafo desde `start`.
- Se generan y rankean vuelos.
- Estado devuelto: `pending_flight_selection`.

---

## HU‑02 – Seleccionar Vuelo

**Como** usuario viajero  
**Quiero** elegir uno de los vuelos propuestos  
**Para** continuar con la búsqueda de alojamiento.

### Criterios de aceptación

- El frontend invoca `/travel/select-flight`.
- El grafo continúa hacia nodo `house`.
- Se calcula presupuesto restante.
- Se generan alojamientos compatibles.
- Estado devuelto:
  - `pending_house_selection`
  - o `no_accommodation_budget`.

### Escenario alternativo

- Si no existen alojamientos dentro del presupuesto:
  - Estado: `no_accommodation_budget`.
  - Se muestra mensaje claro.
  - El usuario puede volver a elegir vuelo.

---

## HU‑03 – Seleccionar Alojamiento

**Como** usuario viajero  
**Quiero** elegir un alojamiento  
**Para** generar mi plan final de viaje.

### Criterios de aceptación

- El frontend invoca `/travel/select-house`.
- El grafo ejecuta nodo `finalize`.
- Se genera documento final en Markdown.
- Estado devuelto: `completed`.

---

# 🧠 Épica 2 – Refinamiento y Revisión (HITL)

---

## HU‑04 – Revisar Redacción del Plan

**Como** usuario  
**Quiero** solicitar una mejora en la redacción del plan  
**Para** obtener una versión más clara o ajustada.

### Criterios de aceptación

- El usuario envía comentario.
- Se invoca `/travel/review`.
- El nodo `review` enruta a `finalize`.
- Se regenera el documento.
- Vuelo y alojamiento no cambian.
- Estado devuelto: `completed`.

---

## HU‑05 – Cambiar Criterios del Viaje

**Como** usuario  
**Quiero** modificar características del alojamiento o vuelo  
**Para** refinar el resultado sin reiniciar todo el proceso.

### Criterios de aceptación

- El comentario se envía al módulo LLM.
- Se extraen restricciones estructuradas.
- El grafo enruta según `review_type`.
- Se re‑ejecuta nodo `flight` o `house`.
- Se devuelven nuevas opciones.
- No se realizan selecciones automáticas.

Estados posibles tras ejecución:
- `pending_house_selection`
- `pending_flight_selection`
- `error`

---

# 🧠 Épica 3 – Interpretación Semántica (LLM)

---

## HU‑06 – Interpretar Restricciones en Lenguaje Natural

**Como** usuario  
**Quiero** escribir restricciones en lenguaje natural  
**Para** no tener que usar filtros técnicos.

### Criterios de aceptación

- Soporte en español e inglés.
- Reconoce:
  - bathrooms
  - bedrooms
  - beds
  - max_guests
- Devuelve JSON válido.
- Se aplica filtrado dinámico.
- No se altera selección sin confirmación humana.

---

# ⚠️ Épica 4 – Manejo de Presupuesto

---

## HU‑07 – Gestionar Presupuesto Insuficiente

**Como** usuario  
**Quiero** recibir aviso si el presupuesto restante no permite alojamientos  
**Para** poder elegir otro vuelo o ajustar mi presupuesto.

### Criterios de aceptación

- El nodo `house` detecta ausencia de opciones.
- Devuelve estado `no_accommodation_budget`.
- El frontend muestra mensaje claro.
- El flujo vuelve a selección de vuelos.
- No se muestra pantalla vacía.

---

# 🏗️ Épica 5 – Arquitectura y Estado

---

## HU‑08 – Flujo Dirigido por Estado

**Como** sistema  
**Quiero** que cada fase devuelva un estado explícito  
**Para** que el frontend renderice correctamente cada paso.

### Estados soportados

- `pending_flight_selection`
- `pending_house_selection`
- `completed`
- `no_accommodation_budget`
- `error`

El estado se gestiona mediante `TravelState` dentro de LangGraph.

---

# 🚫 Funcionalidades No Incluidas en el MVP

- Persistencia en base de datos
- Versionado de itinerarios
- Gestión multiusuario
- Iteraciones automáticas Generador ↔ Crítico
- Infraestructura distribuida
- Supervisor externo formal

---

# ✅ Conclusión

Las historias de usuario están alineadas con la implementación actual:

- Orquestación declarativa con LangGraph
- Flujo controlado por estado
- HITL real
- Integración LLM para interpretación semántica
- Selección explícita del usuario
