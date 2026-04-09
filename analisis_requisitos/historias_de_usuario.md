# Historias de Usuario Refinadas – MVP Multi‑Agente

---

## 🧱 Épica 1 – Orquestación del Flujo Iterativo

---

### HU‑01 – Definición de Flujo Base en LangGraph

**Como** Arquitecto del sistema  
**Quiero** definir un flujo simple en LangGraph con nodos  
`Generador → Crítico → Decisión`  
**Para** validar la dinámica iterativa del MVP.

**Criterios de aceptación:**
- El grafo contiene nodos explícitos.
- Existe transición condicional basada en contador.
- El flujo puede ejecutarse al menos una iteración completa.

---

### HU‑02 – Límite Configurable de Iteraciones

**Como** Orquestador LangGraph  
**Quiero** limitar el número de iteraciones a un máximo configurable (N)  
**Para** evitar loops infinitos y controlar costos.

**Criterios de aceptación:**
- N es configurable vía archivo o variable.
- El ciclo se detiene automáticamente al alcanzar N.
- El estado final pasa a `FINAL_CANDIDATE`.

---

### HU‑03 – Reenvío Automático de Feedback

**Como** Orquestador LangGraph  
**Quiero** reenviar automáticamente el feedback del crítico al generador  
**Para** lograr refinamiento iterativo controlado.

**Criterios de aceptación:**
- El feedback se inyecta como contexto estructurado.
- El contador de iteraciones se incrementa correctamente.
- No se pierde historial previo.

---

## 🤖 Épica 2 – Agentes Especializados

---

### HU‑04 – Generación Estructurada de Itinerario

**Como** Agente Generador  
**Quiero** producir un itinerario estructurado en JSON validado  
**Para** que el agente crítico pueda evaluarlo automáticamente.

**Criterios de aceptación:**
- El output cumple un schema mínimo.
- Contiene días, actividades y justificación.
- Es parseable sin errores.

---

### HU‑05 – Evaluación Estructurada del Itinerario

**Como** Agente Crítico  
**Quiero** devolver retroalimentación clara y accionable en formato estructurado  
**Para** permitir refinamiento automático.

**Criterios de aceptación:**
- El feedback incluye:
  - Problemas detectados
  - Recomendaciones concretas
- El formato es consistente.
- Puede ser reutilizado por el Generador sin transformación manual.

---

## 👤 Épica 3 – Supervisión Humana (HITL)

---

### HU‑06 – Revisión Humana Final

**Como** Supervisor humano (HITL)  
**Quiero** revisar el itinerario final antes de entregarlo  
**Para** validar manualmente el resultado.

**Criterios de aceptación:**
- Se muestra la versión final.
- Se permite aprobar o rechazar.
- Se registra la decisión.

---

### HU‑07 – Finalización Manual del Ciclo

**Como** Supervisor humano  
**Quiero** poder forzar la finalización del ciclo iterativo  
**Para** tener control manual del flujo.

**Criterios de aceptación:**
- Puede ejecutarse en cualquier iteración.
- Detiene el grafo inmediatamente.
- Marca versión actual como candidata final.

---

## 💾 Épica 4 – Estado, Memoria y Persistencia

---

### HU‑08 – Memoria de Sesión Activa

**Como** Módulo de memoria  
**Quiero** almacenar contexto del usuario y última versión  
**Para** mantener continuidad durante la sesión.

**Criterios de aceptación:**
- Se almacena input original.
- Se almacena historial de versiones.
- Se mantiene contador de iteraciones.

---

### HU‑09 – Persistencia Final Básica

**Como** Servicio de persistencia  
**Quiero** guardar el resultado final en almacenamiento ligero  
**Para** garantizar trazabilidad mínima.

**Criterios de aceptación:**
- Se guarda versión final aprobada.
- Se incluye metadata básica (fecha, iteraciones).
- Se confirma almacenamiento exitoso.

---

## 📊 Épica 5 – Observabilidad y Robustez

---

### HU‑10 – Logging Básico del Sistema

**Como** Sistema de logging  
**Quiero** registrar entradas, salidas y número de iteraciones  
**Para** facilitar debugging.

**Criterios de aceptación:**
- Cada ejecución tiene ID de sesión.
- Se registran errores.
- Se registran iteraciones realizadas.

---

### HU‑11 – Manejo Básico de Errores

**Como** Orquestador LangGraph  
**Quiero** capturar errores de ejecución de agentes  
**Para** devolver mensajes controlados y mantener resiliencia básica.

**Criterios de aceptación:**
- Excepciones capturadas por nodo.
- Error registrado.
- Estado pasa a `FAILED`.

---

## ⚙️ Épica 6 – Configuración y Modularidad

---

### HU‑12 – Configuración Externa de Prompts

**Como** Configuración de prompts  
**Quiero** definir prompts en archivos configurables  
**Para** permitir ajustes sin modificar código.

**Criterios de aceptación:**
- Prompts separados del código.
- Cargados dinámicamente al iniciar.
- Modificables sin recompilar.

---

### HU‑13 – Aplicación Modular Única

**Como** Arquitecto del sistema  
**Quiero** mantener todos los componentes en una única aplicación modular  
**Para** simplificar despliegue del MVP.

**Criterios de aceptación:**
- Separación por módulos internos.
- No requiere microservicios.
- Puede desplegarse como única instancia.
