# ✈️ DevAgents Lab · Planificador Inteligente Multi‑Agente
## Evidencia del Uso de IA en el Ciclo de Vida del Software

Este documento recopila y organiza los **prompts utilizados durante el desarrollo del proyecto**, estructurados según las fases del ciclo de vida del software (SDLC).

El objetivo es **evidenciar el uso estratégico de IA** en:

- ✅ Análisis de requisitos  
- ✅ Diseño y arquitectura  
- ✅ Desarrollo  
- ✅ Validación arquitectónica  
- ✅ Documentación  

No se utilizó la IA como simple generador de código, sino como **asistente estructural, analítico y crítico** a lo largo de todo el proceso.

---

# 🧭 1️⃣ Fase de Contextualización del Proyecto

## 🎯 Objetivo
Establecer claramente el problema, el alcance y el enfoque multi‑agente antes de iniciar análisis y diseño.

## 🧠 Uso de IA
Se utilizó para:
- Definir el enfoque del MVP
- Alinear el sistema con la propuesta académica
- Establecer objetivos y restricciones claras

---

## 📌 Prompt 1 — Contexto General del Proyecto
Prompt de Contexto – Proyecto DevAgents Lab Propuesta 4: Planificador Inteligente de Viajes con Sistema Multi‑Agente

Estoy desarrollando un MVP de un Planificador Inteligente de Viajes como proyecto integrador de DevAgents Lab.

El objetivo es diseñar un sistema multi‑agente orquestado con LangGraph que genere, critique y refine itinerarios de viaje personalizados de forma iterativa, manteniendo supervisión humana (HITL).

🎯 Problema a resolver Los usuarios quieren organizar viajes optimizados según: destino fechas presupuesto intereses (cultura, gastronomía, naturaleza, ocio, etc.) restricciones (tiempo disponible, transporte, horarios)

El sistema debe generar un plan coherente y justificar sus decisiones, permitiendo revisión humana antes de la propuesta final.


Copy
Text

---

# 📊 2️⃣ Fase de Análisis de Requisitos

## 🎯 Objetivo
Realizar un análisis estructurado del MVP desde una perspectiva:
- Funcional
- Técnica
- Estratégica
- De riesgos
- De métricas (KPIs)

## 🧠 Uso de IA
Se utilizó como **analista senior virtual**, solicitando:
- Identificación de brechas
- Detección de riesgos
- Definición de límites
- Métricas de éxito medibles
- Recomendaciones de mejora

---

## 📌 Prompt 2 — Análisis Estructurado del Sistema
Actúa como analista senior de producto y arquitectura de software especializado en sistemas multi‑agente.

A partir de los siguientes casos de uso y contexto del proyecto, realiza un análisis estructurado del sistema.

🎯 Objetivo del análisis Determinar con claridad: Alcance funcional del MVP Alcance técnico Objetivos estratégicos y operativos Límites del sistema Supuestos clave Riesgos principales Métricas de éxito (KPIs) Dependencias técnicas Posibles brechas o inconsistencias en el diseño Recomendaciones de mejora para robustecer el MVP

📥 INFORMACIÓN DE ENTRADA [AQUÍ PEGAR LOS CASOS DE USO] [AQUÍ PEGAR EL CONTEXTO DEL PROYECTO]

📤 FORMATO DE RESPUESTA OBLIGATORIO (estructura numerada del 1️⃣ al 9️⃣ con análisis técnico, crítico y orientado a arquitectura)

🔎 Nivel de profundidad esperado El análisis debe ser: Técnico Crítico Orientado a arquitectura Enfocado en MVP realista Sin explicaciones genéricas Sin repetir literalmente los casos de uso

Si detectas ambigüedades, explícitalas como riesgos o supuestos.


Copy
Text

---

# 🏗 3️⃣ Fase de Diseño y Arquitectura

## 🎯 Objetivo
Definir una arquitectura:
- Modular
- Multi‑agente
- Escalable
- Con separación clara de responsabilidades
- Preparada para producción

## 🧠 Uso de IA
Se utilizó para:
- Diseñar backend y frontend desacoplados
- Definir estructura de carpetas
- Establecer agentes especializados
- Diseñar flujo de orquestación obligatorio
- Definir reglas críticas de negocio
- Forzar cumplimiento de requisitos técnicos estrictos

---

## 📌 Prompt 3 — Implementación Completa Backend + Frontend
Quiero que implementes un sistema completo dividido en Backend y Frontend, siguiendo una arquitectura modular multi‑agente para búsqueda y análisis de vuelos y alojamientos.

No usar pseudocódigo. Código real, ejecutable y modular. Preparado para producción.

🎯 OBJETIVO GENERAL (Se detallan reglas de negocio completas incluyendo validaciones, scraping real, HITL, flujo obligatorio y reglas críticas)

🖥 PARTE 1 — BACKEND Python 3.11+ FastAPI Pydantic Async/await httpx o Playwright Arquitectura modular

(Estructura completa de carpetas backend)

✈️ Modelo de Entrada obligatorio: class FlightRequest(BaseModel): origin_airport: str destination_country: str departure_date: date return_date: date passengers: int max_budget: float

🤖 AGENTES BACKEND FlightPlannerAgent FlightAnalystAgent HousePlannerAgent HouseAnalystAgent DocumentalistAgent

🔁 Orquestador Backend (Flujo obligatorio numerado del 1 al 12)

❗ Regla Crítica Backend Si no hay vuelos: "No hemos encontrado ofertas con tus requisitos" Y no ejecutar búsqueda de casas.

🌐 PARTE 2 — FRONTEND React o Next.js TypeScript Arquitectura modular (estructura detallada de frontend y flujo completo)

✅ RESULTADO FINAL ESPERADO Ejecución con: uvicorn main:app --reload npm run dev Flujo completo funcional Sin pseudocódigo Sin omitir archivos


Copy
Text

---

# 🔍 4️⃣ Fase de Validación Arquitectónica

## 🎯 Objetivo
Verificar que la implementación cumple con las directrices arquitectónicas definidas.

## 🧠 Uso de IA
Se utilizó como:
- Revisor arquitectónico
- Auditor técnico
- Evaluador de coherencia estructural

---

## 📌 Prompt 4 — Revisión de Arquitectura
revisa mi codigo y dime si sigue estas indicaciones orientativas que cree:

1️⃣ Visión General de Arquitectura Arquitectura modular orientada a agentes Orquestación centralizada Separación clara entre: Presentación Lógica multi‑agente Persistencia Servicios externos

2️⃣ Componentes Principales (Capa de presentación, API, Orquestador, Agentes IA, HITL, Persistencia)

3️⃣ Flujo de Datos (Flujo completo desde Usuario hasta Base de Datos)

4️⃣ Modelo de Dominio Simplificado (TravelRequest, TravelPlan, DayPlan, Activity)

5️⃣ Arquitectura Técnica (Python + FastAPI + LangGraph + PostgreSQL + React)

6️⃣ Justificación Arquitectónica (tabla de decisiones y justificaciones)

7️⃣ Escalabilidad Futura (agente optimizador, cache semántica, arquitectura por eventos)

✅ Resultado esperado: Validar diseño modular, separación de responsabilidades, multi‑agencia clara y control mediante agente crítico y HITL.


Copy
Text

---

# 📚 5️⃣ Fase de Documentación Técnica

## 🎯 Objetivo
Generar documentación exhaustiva alineada con buenas prácticas de ingeniería.

## 🧠 Uso de IA
Se utilizó para:
- Explicar arquitectura
- Analizar patrones
- Documentar estructuras de datos
- Relacionar código con lógica de negocio
- Redactar documentación técnica formal

---

## 📌 Prompt 5 — Documentación Exhaustiva
Elaborar una documentación exhaustiva de todas las secciones de código proporcionadas, que abarque la arquitectura, las mejores prácticas, los patrones, las estructuras de datos y los análisis de negocio


Copy
Text

---

# ✅ Conclusión

A lo largo del proyecto, la IA fue utilizada estratégicamente en múltiples fases del ciclo de vida:

| Fase | Uso de IA |
|------|-----------|
| Contextualización | Definición del problema y alcance |
| Requisitos | Análisis estructurado y detección de riesgos |
| Diseño | Arquitectura modular multi‑agente |
| Desarrollo | Generación estructurada de código productivo |
| Validación | Auditoría arquitectónica |
| Documentación | Redacción técnica exhaustiva |

El enfoque demuestra:

- ✅ Orquestación consciente de agentes  
- ✅ Separación clara entre IA y lógica determinista  
- ✅ Control humano (HITL)  
- ✅ Diseño modular y escalable  
- ✅ Uso crítico de la IA, no uso indiscriminado  

---

**Este documento constituye evidencia formal del uso de IA en el ciclo completo de desarrollo del software.**
