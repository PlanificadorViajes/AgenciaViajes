
# Casos de Uso Refinados  
## MVP – Planificador Inteligente de Viajes (Sistema Multi‑Agente con LangGraph)

> Versión refactorizada con:
> - Separación clara entre casos de negocio y procesos internos
> - Eliminación de redundancias
> - Mejor alineación con arquitectura basada en estados
> - Coherencia con flujo Generador → Crítico → Decisión → HITL

---

# 📌 CASOS DE USO DE NEGOCIO

---

## CU‑01 – Crear Solicitud de Itinerario

**Actor principal:** Usuario viajero  
**Descripción:** El usuario proporciona la información necesaria para generar un itinerario personalizado.

### Precondiciones
- Sistema disponible.
- Usuario con acceso activo a la aplicación.

### Flujo Principal
1. El usuario ingresa:
   - Destino
   - Fechas
   - Presupuesto (opcional en MVP)
   - Intereses
   - Restricciones
2. El sistema valida campos mínimos obligatorios.
3. Se crea una sesión activa con estado `CREATED`.
4. Se inicia el flujo de generación automática.

### Flujos Alternativos
- **A1 – Datos incompletos:**  
  El sistema solicita completar la información requerida.

### Postcondiciones
- Sesión inicializada.
- Estado del proceso: `CREATED`.

---

## CU‑02 – Ejecutar Generación Inicial

**Actor principal:** Sistema (Orquestador LangGraph)  
**Actores secundarios:** Agente Generador  

**Descripción:** El sistema genera la primera versión estructurada del itinerario.

### Precondiciones
- Existe sesión en estado `CREATED`.

### Flujo Principal
1. El orquestador construye el contexto desde memoria.
2. Envía solicitud al Agente Generador.
3. El Generador produce itinerario estructurado (JSON válido).
4. El sistema valida estructura.
5. Se almacena como `version = 1`.
6. Estado pasa a `GENERATED`.

### Flujos Alternativos
- **A1 – Error de generación:**  
  - Se registra en log.  
  - Estado pasa a `FAILED`.

- **A2 – Estructura inválida:**  
  - Se solicita regeneración automática (si permitido).  
  - Si falla nuevamente → `FAILED`.

### Postcondiciones
- Versión inicial almacenada.
- Lista para evaluación.

---

## CU‑03 – Evaluar Itinerario

**Actor principal:** Sistema (Orquestador)  
**Actor secundario:** Agente Crítico  

**Descripción:** El sistema evalúa calidad, coherencia y cumplimiento de restricciones.

### Precondiciones
- Existe versión generada.
- Estado `GENERATED` o `ITERATING`.

### Flujo Principal
1. El orquestador envía versión actual al Crítico.
2. El Crítico devuelve feedback estructurado.
3. Se valida formato del feedback.
4. Se almacena en memoria.
5. Estado pasa a `EVALUATED`.

### Flujos Alternativos
- **A1 – Error en evaluación:**  
  Estado → `FAILED`.

- **A2 – Feedback inválido:**  
  Reintento configurable o fallo controlado.

### Postcondiciones
- Feedback disponible.
- Lista para decisión de iteración.

---

## CU‑04 – Ejecutar Ciclo de Refinamiento Automático

**Actor principal:** Sistema (Orquestador)  
**Actores secundarios:** Generador, Crítico  

**Descripción:** Ejecuta iteraciones automáticas hasta alcanzar criterio de parada.

### Precondiciones
- Estado `EVALUATED`.
- Iteraciones < N máximo.

### Flujo Principal
1. El sistema evalúa condición de parada:
   - ¿Iteraciones ≥ N?
   - ¿Supervisor forzó finalización?
2. Si no se cumple condición de salida:
   - Envía feedback al Generador.
   - Genera nueva versión.
   - Incrementa contador.
   - Evalúa nuevamente con Crítico.
3. Repite hasta alcanzar condición de salida.
4. Estado pasa a `FINAL_CANDIDATE`.

### Flujos Alternativos
- **A1 – Se alcanza máximo N:**  
  Se detiene automáticamente.

- **A2 – Error intermedio:**  
  Estado → `FAILED`.

### Postcondiciones
- Versión candidata final disponible.

---

## CU‑05 – Revisión Humana (HITL)

**Actor principal:** Supervisor humano  

**Descripción:** Validación manual antes de entrega final.

### Precondiciones
- Estado `FINAL_CANDIDATE`.

### Flujo Principal
1. El sistema presenta:
   - Última versión.
   - Historial resumido de iteraciones.
2. El supervisor:
   - Aprueba → Estado `APPROVED`
   - Rechaza → Estado `REJECTED`

### Flujos Alternativos
- **A1 – Rechazo:**  
  Se reactiva ciclo de refinamiento manual (contador puede reiniciarse o continuar según configuración).

### Postcondiciones
- Itinerario aprobado o reenviado a iteración.

---

## CU‑06 – Forzar Finalización Manual

**Actor principal:** Supervisor humano  

**Descripción:** Permite detener iteraciones activas y aceptar versión actual.

### Precondiciones
- Estado `ITERATING`.

### Flujo Principal
1. Supervisor solicita finalización.
2. Orquestador detiene ciclo.
3. Estado → `FINAL_CANDIDATE`.

### Postcondiciones
- Versión actual marcada como candidata final.

---

## CU‑07 – Persistir Itinerario Final

**Actor principal:** Sistema  
**Actor secundario:** Módulo de Persistencia  

**Descripción:** Guarda el resultado aprobado.

### Precondiciones
- Estado `APPROVED`.

### Flujo Principal
1. Se construye objeto final con:
   - Datos de usuario
   - Versión final
   - Número de iteraciones
2. Se almacena en archivo o base ligera.
3. Estado → `PERSISTED`.

### Flujos Alternativos
- **A1 – Error de guardado:**  
  Se registra en log.  
  Estado → `FAILED_PERSISTENCE`.

### Postcondiciones
- Itinerario almacenado correctamente.

---

# 📌 PROCESOS INTERNOS DEL SISTEMA

*(No visibles como casos de negocio, pero formalizados para arquitectura)*

---

## PI‑01 – Gestión de Estado del Flujo

Estados posibles:

- `CREATED`
- `GENERATED`
- `EVALUATED`
- `ITERATING`
- `FINAL_CANDIDATE`
- `APPROVED`
- `REJECTED`
- `PERSISTED`
- `FAILED`

---

## PI‑02 – Gestión de Memoria de Sesión

- Almacena:
  - Input original
  - Versiones sucesivas
  - Feedback estructurado
  - Contador de iteraciones
- Eliminación automática tras finalización o timeout.

---

## PI‑03 – Manejo Básico de Errores

- Captura de excepciones por nodo.
- Registro en logging.
- Transición a estado `FAILED`.
- Mensaje controlado al usuario o supervisor.

---

# ✅ Resultado del Rediseño

Con esta versión:

- Se eliminan redundancias (límite de iteraciones integrado).
- Se separan claramente:
  - Casos de negocio
  - Procesos técnicos internos
- Se introduce modelo explícito de estados.
- Se mejora alineación con arquitectura LangGraph.
- Se reduce ambigüedad en responsabilidades.

---

# 🏁 Conclusión

Este conjunto de casos de uso es:

- Más coherente arquitectónicamente
- Más mantenible
- Más escalable
- Mejor alineado con sistemas multi‑agente iterativos

Apto para implementación directa en LangGraph con control de estados formal.
```