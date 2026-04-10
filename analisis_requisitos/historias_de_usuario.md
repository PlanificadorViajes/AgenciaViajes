# 📘 Historias de Usuario – Travel Planner MVP  
## Sistema Multi‑Agente con Orquestación Centralizada y HITL

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
  - Fechas
  - Número de pasajeros
  - Presupuesto máximo
- Se valida que los campos obligatorios estén completos.
- El sistema devuelve lista de vuelos.
- Estado devuelto: `pending_flight_selection`.

---

## HU‑02 – Seleccionar Vuelo

**Como** usuario viajero  
**Quiero** elegir uno de los vuelos propuestos  
**Para** continuar con la búsqueda de alojamiento.

### Criterios de aceptación

- El sistema calcula presupuesto restante.
- Genera alojamientos compatibles.
- Devuelve lista de alojamientos.
- Estado devuelto: `pending_house_selection`.

### Escenario alternativo

- Si no existen alojamientos dentro del presupuesto:
  - Estado devuelto: `no_accommodation_budget`.
  - Se muestra mensaje claro.
  - El usuario puede volver a elegir vuelo.

---

## HU‑03 – Seleccionar Alojamiento

**Como** usuario viajero  
**Quiero** elegir un alojamiento  
**Para** generar mi plan final de viaje.

### Criterios de aceptación

- El sistema genera documento final en Markdown.
- Se muestran detalles:
  - Vuelo seleccionado
  - Alojamiento seleccionado
  - Alternativas
  - Desglose presupuestario
- Estado devuelto: `completed`.

---

# 🧠 Épica 2 – Refinamiento y Revisión (HITL)

---

## HU‑04 – Revisar Redacción del Plan

**Como** usuario  
**Quiero** solicitar una mejora en la redacción del plan  
**Para** obtener una versión más clara o ajustada.

### Criterios de aceptación

- El usuario introduce comentario.
- El sistema regenera el documento.
- Vuelo y alojamiento no cambian.
- Estado devuelto: `revised`.

---

## HU‑05 – Cambiar Criterios del Viaje

**Como** usuario  
**Quiero** modificar características del alojamiento o vuelo  
**Para** refinar el resultado sin reiniciar todo el proceso.

### Criterios de aceptación

- El comentario se envía al módulo LLM.
- Se extraen restricciones estructuradas.
- El sistema re‑ejecuta búsqueda correspondiente.
- Devuelve nuevas opciones para confirmación explícita.
- Estado devuelto:
  - `pending_house_selection`
  - `pending_flight_selection`
  - o `error` si no hay coincidencias.

---

# 🧠 Épica 3 – Interpretación Semántica (LLM)

---

## HU‑06 – Interpretar Restricciones en Lenguaje Natural

**Como** usuario  
**Quiero** escribir restricciones en lenguaje natural  
**Para** no tener que usar filtros técnicos.

### Criterios de aceptación

- Soporte en español e inglés.
- El sistema reconoce:
  - bathrooms
  - bedrooms
  - beds
  - max_guests
- Devuelve JSON válido.
- Se aplica filtrado dinámico.
- No se realizan selecciones automáticas sin confirmación.

---

# ⚠️ Épica 4 – Manejo de Presupuesto

---

## HU‑07 – Gestionar Presupuesto Insuficiente

**Como** usuario  
**Quiero** recibir aviso si el presupuesto restante no permite alojamientos  
**Para** poder elegir otro vuelo o ajustar mi presupuesto.

### Criterios de aceptación

- El sistema detecta ausencia de alojamientos.
- Devuelve estado `no_accommodation_budget`.
- El frontend muestra mensaje claro.
- El usuario vuelve a pantalla de vuelos.
- No se muestra pantalla vacía.

---

# 🏗️ Épica 5 – Arquitectura y Estado

---

## HU‑08 – Flujo Dirigido por Estado

**Como** sistema  
**Quiero** que cada fase devuelva un estado explícito  
**Para** que el frontend renderice correctamente cada paso.

### Criterios de aceptación

Estados soportados:

- `pending_flight_selection`
- `pending_house_selection`
- `completed`
- `revised`
- `no_accommodation_budget`
- `error`

---

# 🚫 Funcionalidades NO Incluidas en el MVP

Estas historias NO forman parte del sistema actual:

- Iteraciones automáticas Generador ↔ Crítico.
- Límite configurable de iteraciones.
- Persistencia en base de datos.
- Versionado de itinerarios.
- Gestión multiusuario.
- Supervisor humano separado.
- Memoria persistente de sesión.

---

# ✅ Conclusión

Las historias de usuario actuales reflejan fielmente:

- Flujo secuencial controlado.
- Arquitectura multi‑agente modular.
- HITL real.
- Interpretación semántica mediante LLM.
- Manejo explícito de estados.
- Gestión robusta de presupuesto insuficiente.

Documento completamente alineado con la implementación real.
