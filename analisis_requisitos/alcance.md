# DevAgents Lab – Alcance del MVP  
## Planificador Inteligente de Viajes (Sistema Multi‑Agente con LangGraph)

---

# 1️⃣ Alcance Funcional del MVP

## ✅ Funcionalidades incluidas

- Creación de solicitud de itinerario con datos mínimos:
  - Destino
  - Fechas
  - Presupuesto
  - Intereses
  - Restricciones
- Generación automática de itinerario inicial.
- Evaluación automática mediante agente crítico.
- Ciclo iterativo controlado Generador ↔ Crítico.
- Límite configurable de iteraciones (N).
- Finalización automática por límite.
- Intervención humana (HITL):
  - Revisión y aprobación.
  - Rechazo con nueva iteración.
  - Forzar finalización manual.
- Persistencia básica del resultado final.
- Memoria de sesión activa.
- Logging básico de ejecución y errores.
- Manejo simple de excepciones en agentes.
- Prompts configurables externos.

---

## 🔄 Proceso End-to-End Cubierto

1. Usuario crea solicitud.
2. Orquestador crea sesión activa.
3. Generación → Evaluación → Refinamiento (iterativo).
4. Control por contador de iteraciones.
5. Revisión humana (HITL).
6. Persistencia del resultado final.
7. Registro en logs y cierre del proceso.

---

## 👥 Actores

- Usuario viajero
- Orquestador LangGraph
- Agente Generador
- Agente Crítico
- Supervisor humano (HITL)
- Módulo de memoria
- Servicio de persistencia

---

## 🚫 Fuera de Alcance

- Integraciones reales con APIs externas (Google Maps, Skyscanner, etc.).
- Optimización matemática real de rutas.
- Estimación financiera precisa.
- Persistencia avanzada multiusuario.
- Autenticación y autorización.
- Interfaz web compleja.
- Perfilado persistente del usuario.
- Evaluación automática cuantitativa avanzada de calidad.

---

# 2️⃣ Alcance Técnico

## 🏗️ Arquitectura

- Arquitectura modular monolítica.
- Orquestación mediante **LangGraph**.
- Flujo dirigido por grafo con nodos:

  - Generador  
  - Crítico  
  - Decisión  
  - HITL  
  - Persistencia  

---

## 🧩 Componentes Principales

- Graph Orchestrator
- Agent: Generator
- Agent: Critic
- Session Memory Module
- Persistence Module
- Logging Module
- Prompt Configuration Layer

---

## 🔁 Tipo de Orquestación

Control explícito de estados en LangGraph con transiciones condicionales:

- Si `iteraciones < N` → volver a Generador.
- Si `iteraciones ≥ N` → finalizar automáticamente.
- Si HITL rechaza → reiniciar ciclo.
- Si HITL fuerza cierre → finalizar inmediatamente.

---

## 🧠 Gestión de Memoria

Memoria en sesión (in-memory).

Almacena:

- Input del usuario.
- Versiones del itinerario.
- Feedback estructurado.
- Contador de iteraciones.

No es persistente entre reinicios del sistema.

---

## ⚠️ Manejo de Errores

- Try/catch a nivel de nodo.
- Registro en log.
- Mensaje controlado al usuario o supervisor.

No incluye:

- Retries automáticos.
- Circuit breakers.
- Clasificación avanzada de errores.

---

## 💾 Persistencia

- Almacenamiento simple:
  - Archivo JSON  
  - Base de datos ligera  

- Solo se guarda la versión final.
- No hay versionado histórico completo en el MVP.

---

# 3️⃣ Objetivos del Sistema

## 🎯 Estratégicos

- Validar viabilidad de arquitectura multi‑agente con LangGraph.
- Demostrar mejora iterativa frente a generación única.
- Incorporar HITL como capa de gobernanza.
- Servir como base experimental para futuras extensiones.

---

## ⚙️ Operativos

- Implementar ciclo iterativo estable.
- Garantizar límite de iteraciones configurable.
- Asegurar salida estructurada consistente.
- Permitir intervención humana sin romper el flujo.
- Registrar trazabilidad mínima del proceso.

---

# 4️⃣ Límites del Sistema

## 🔒 Límites Funcionales

- No garantiza exactitud real de horarios o precios.
- No valida datos externos.
- No asegura coherencia geográfica real.

---

## 🧱 Límites Técnicos

- Memoria volátil.
- Sin paralelización de agentes.
- Dependencia directa del LLM.
- No hay versionado fuerte de estados.

---

## ⚙️ Límites Operativos

- Máximo N iteraciones.
- HITL obligatorio antes de entrega.
- Finalización manual posible en cualquier momento.

---

# 5️⃣ Supuestos Clave

## 🧪 Supuestos Técnicos

- El LLM responde en formato estructurado consistente.
- El feedback del crítico es accionable.
- LangGraph maneja correctamente estados cíclicos.

---

## 👤 Supuestos de Usuario

- El usuario entrega datos mínimos válidos.
- El supervisor humano tiene criterio suficiente para validar.

---

## 🖥️ Supuestos de Infraestructura

- Sistema mono-instancia.
- Baja concurrencia.
- Persistencia local suficiente para MVP.

---

# 6️⃣ Riesgos Identificados

## 🛠️ Técnicos

- Inconsistencia en formato JSON del generador.
- Loop infinito si falla la lógica de decisión.
- Pérdida de sesión en reinicio.
- Acoplamiento fuerte entre prompts y lógica.

---

## 📉 Calidad del Output

- Refinamientos que no mejoran realmente.
- Crítico poco exigente o demasiado severo.
- Deriva semántica entre versiones.

---

## 📈 Escalabilidad

- No soporta múltiples sesiones concurrentes de forma robusta.
- Memoria en RAM no escalable.
- Sin separación de workers.

---

## 👤 Experiencia de Usuario

- Latencia acumulativa por iteraciones.
- Falta de visibilidad del progreso.
- Falta de explicación clara de los cambios.

---

## 🧑‍⚖️ Gobernanza / HITL

- Criterios de aprobación no definidos.
- Subjetividad del supervisor no trazada.
- No hay auditoría estructurada del rechazo.

---

# 7️⃣ Métricas de Éxito (KPIs)

## 📊 Calidad

- % de itinerarios aprobados en primera revisión.
- Promedio de mejoras aceptadas por iteración.
- Score de coherencia estructural (validación JSON).

---

## 🔁 Iteración

- Número promedio de iteraciones por solicitud.
- % de procesos que alcanzan máximo N.
- % de finalizaciones manuales.

---

## ⚠️ Robustez

- Tasa de errores por agente.
- Tasa de fallos de parsing estructural.
- % de sesiones interrumpidas.

---

## ⏱️ Rendimiento

- Tiempo total promedio de generación.
- Tiempo por iteración.
- Latencia total hasta aprobación.

---

## 🔄 Consistencia

- Diferencia estructural entre versiones consecutivas.
- Ratio de cambios aplicados vs sugeridos.

---

# 8️⃣ Brechas o Inconsistencias Detectadas

## 🔁 Flujo Iterativo

- Se menciona Agente Refinador, pero en la definición técnica solo existen Generador y Crítico.
- Ambigüedad sobre si el Refinador es un agente separado o el mismo Generador con feedback.

---

## 🧠 Gestión de Memoria

- No se define estructura formal del estado.
- No se define política de limpieza de sesiones.

---

## ⚠️ Manejo de Errores

- No se define comportamiento tras error intermedio.
- No hay estrategia de retry.
- No hay fallback si el crítico falla.

---

## 👤 Supervisión Humana

- No hay criterios formales de aprobación.
- No está claro si el supervisor puede editar directamente.
- No se define cómo se integra feedback manual al ciclo.

---

## 💾 Persistencia

- Solo se guarda versión final.
- No se almacenan versiones intermedias.
- No se define esquema de almacenamiento formal.

---

# 9️⃣ Recomendaciones de Mejora

## 🔴 Alta Prioridad

1. Definir contrato estructural estricto (schema JSON validado).
2. Unificar concepto Generador/Refinador.
3. Definir modelo de estado explícito en LangGraph.
4. Validar estructura antes de enviar al crítico.
5. Registrar todas las versiones en persistencia mínima.
6. Definir criterios formales de aprobación HITL.

---

## 🟡 Media Prioridad

1. Implementar retry simple ante fallos transitorios.
2. Agregar métrica automática heurística de calidad.
3. Separar memoria de sesión de memoria del grafo.
4. Añadir trazabilidad estructurada (ID de versión).

---

## 🟢 Baja Prioridad

1. Añadir scoring automático comparativo entre versiones.
2. Introducir feedback cuantitativo del supervisor.
3. Preparar abstracción para futura integración con APIs externas.
4. Diseñar interfaz visual mínima para seguimiento del ciclo.

---

# ✅ Conclusión Arquitectónica

El MVP está bien delimitado y es coherente como experimento académico multi‑agente.

Los principales puntos críticos son:

- Consistencia estructural del output.
- Gobernanza del ciclo iterativo.
- Robustez del manejo de estado en LangGraph.

Con contratos de datos claros y reglas explícitas de decisión, el MVP es sólido como base experimental y extensible.
