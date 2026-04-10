# 📚 Casos de Uso  
## Travel Planner MVP – Sistema Multi‑Agente con Orquestación Centralizada

---

# 📌 Introducción

Este documento describe los casos de uso reales del sistema actualmente implementado.

El sistema no utiliza LangGraph ni ciclo iterativo automático Generador–Crítico.  
Se basa en una orquestación centralizada mediante `TravelOrchestrator` y un flujo dirigido por estados (`status`).

---

# ✅ CASOS DE USO DE NEGOCIO

---

## CU‑01 – Crear Solicitud de Viaje

**Actor principal:** Usuario viajero  
**Descripción:** El usuario introduce los datos necesarios para iniciar la planificación.

### Precondiciones
- Sistema operativo y accesible.
- Usuario con acceso al frontend.

### Flujo Principal
1. El usuario introduce:
   - Aeropuerto de origen
   - País de destino
   - Ciudad (opcional)
   - Fechas
   - Número de pasajeros
   - Presupuesto máximo
2. El frontend envía solicitud al backend.
3. El sistema genera vuelos.
4. Estado devuelto: `pending_flight_selection`.

### Postcondiciones
- Lista de vuelos disponibles para selección.

---

## CU‑02 – Seleccionar Vuelo

**Actor principal:** Usuario viajero  
**Actor secundario:** Sistema (FlightPlanner + FlightAnalyst)

### Precondiciones
- Estado actual: `pending_flight_selection`.

### Flujo Principal
1. El usuario selecciona un vuelo.
2. El sistema:
   - Calcula presupuesto restante.
   - Genera alojamientos sintéticos.
   - Aplica scoring.
3. Estado devuelto:
   - `pending_house_selection`
   - O `no_accommodation_budget` si no hay opciones.

### Flujos Alternativos

**A1 – Presupuesto insuficiente**
- El sistema devuelve estado `no_accommodation_budget`.
- El frontend muestra mensaje.
- Se vuelve a selección de vuelos.

### Postcondiciones
- Lista de alojamientos disponibles o mensaje de presupuesto insuficiente.

---

## CU‑03 – Seleccionar Alojamiento

**Actor principal:** Usuario viajero  

### Precondiciones
- Estado actual: `pending_house_selection`.

### Flujo Principal
1. El usuario selecciona alojamiento.
2. El sistema genera plan final en Markdown.
3. Estado devuelto: `completed`.

### Postcondiciones
- Documento final generado.

---

## CU‑04 – Revisar Redacción (HITL Editorial)

**Actor principal:** Usuario viajero  

### Precondiciones
- Estado actual: `completed`.

### Flujo Principal
1. Usuario introduce comentario editorial.
2. Backend regenera el documento final.
3. Estado devuelto: `revised`.

### Postcondiciones
- Nuevo documento final generado.
- Vuelo y alojamiento no cambian.

---

## CU‑05 – Cambiar Criterios (HITL Semántico)

**Actor principal:** Usuario viajero  
**Actor secundario:** LLM Constraint Extractor  

### Precondiciones
- Estado actual: `completed`.

### Flujo Principal
1. Usuario introduce comentario (ej: “quiero 1 baño”).
2. El sistema:
   - Envía comentario al LLM.
   - Extrae restricciones estructuradas.
   - Reejecuta búsqueda.
3. Devuelve:
   - `pending_house_selection` si hay resultados.
   - `error` si no hay coincidencias.

### Postcondiciones
- Nuevas opciones disponibles para confirmación explícita.

---

# 🧠 PROCESOS INTERNOS RELEVANTES

---

## PI‑01 – Extracción Semántica de Restricciones

El módulo LLM:

- Interpreta texto libre.
- Devuelve JSON estructurado.
- Soporta español e inglés.
- Permite filtrado dinámico.

No existe iteración automática.

---

## PI‑02 – Gestión de Estados

Estados reales del sistema:

- `pending_flight_selection`
- `pending_house_selection`
- `completed`
- `revised`
- `no_accommodation_budget`
- `error`

El frontend reacciona explícitamente a cada uno.

---

## PI‑03 – Manejo de Presupuesto Insuficiente

Si no existen alojamientos dentro del presupuesto restante:

1. Backend devuelve `no_accommodation_budget`.
2. Frontend muestra mensaje.
3. Se vuelve a selección de vuelos.
4. No hay pantalla en blanco.

---

# 🚫 Funcionalidades NO Implementadas

El sistema actual NO incluye:

- Ciclo automático Generador ↔ Crítico.
- Iteraciones controladas por contador N.
- Supervisor formal separado.
- Persistencia de sesiones.
- Versionado de itinerarios.
- Gestión de memoria persistente.
- Estados como `ITERATING`, `APPROVED`, `FINAL_CANDIDATE`.

---

# ✅ Conclusión

Los casos de uso reflejan fielmente el sistema implementado:

- Flujo secuencial controlado.
- Selección explícita del usuario.
- Integración semántica mediante LLM.
- HITL real.
- Manejo robusto de estados.
- Arquitectura modular multi‑agente sin sobre‑ingeniería.

Este documento está alineado con la implementación actual del código.
