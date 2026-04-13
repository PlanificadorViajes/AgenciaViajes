# ✈️ DevAgents Lab · Planificador Inteligente Multi‑Agente
## Evidencia del Uso de IA en el Ciclo de Vida del Software

Este documento recopila y organiza todos los prompts utilizados durante el desarrollo del proyecto, estructurados según las fases del ciclo de vida del software (SDLC).

El objetivo es evidenciar el uso estratégico y justificado de IA en:

- ✅ Análisis de requisitos  
- ✅ Diseño y arquitectura  
- ✅ Desarrollo  
- ✅ Validación arquitectónica  
- ✅ Documentación  

La IA no se utilizó como simple generador de código, sino como asistente analítico, arquitectónico y crítico en distintas fases del proyecto.

---

# 🧭 1️⃣ Contextualización del Proyecto

## 🎯 Objetivo

Definir claramente el problema, el alcance y el enfoque multi‑agente antes de iniciar el análisis y diseño del sistema.

## 🧠 Uso de IA

Se utilizó para:
- Formalizar el objetivo del MVP
- Alinear el sistema con la propuesta académica
- Establecer restricciones y expectativas desde el inicio

---

## 📌 Prompt 1 — Contexto General del Proyecto
Prompt de Contexto – Proyecto DevAgents Lab Propuesta 4: Planificador Inteligente de Viajes con Sistema Multi‑Agente Estoy desarrollando un MVP de un Planificador Inteligente de Viajes como proyecto integrador de DevAgents Lab. El objetivo es diseñar un sistema multi‑agente orquestado con LangGraph que genere, critique y refine itinerarios de viaje personalizados de forma iterativa, manteniendo supervisión humana (HITL). 🎯 Problema a resolver Los usuarios quieren organizar viajes optimizados según: destino fechas presupuesto intereses (cultura, gastronomía, naturaleza, ocio, etc.) restricciones (tiempo disponible, transporte, horarios) El sistema debe generar un plan coherente y justificar sus decisiones, permitiendo revisión humana antes de la propuesta final.

---

# 📊 2️⃣ Análisis de Requisitos

## 🎯 Objetivo

Realizar un análisis estructurado del MVP desde una perspectiva funcional, técnica y estratégica.

## 🧠 Uso de IA

Se utilizó como analista senior virtual para:
- Determinar alcance funcional y técnico
- Identificar riesgos
- Definir KPIs medibles
- Detectar brechas de diseño
- Formular recomendaciones de mejora

---

## 📌 Prompt 2 — Análisis Estructurado del Sistema
Actúa como analista senior de producto y arquitectura de software especializado en sistemas multi‑agente. A partir de los siguientes casos de uso y contexto del proyecto, realiza un análisis estructurado del sistema. 🎯 Objetivo del análisis Determinar con claridad: Alcance funcional del MVP Alcance técnico Objetivos estratégicos y operativos Límites del sistema Supuestos clave Riesgos principales Métricas de éxito (KPIs) Dependencias técnicas Posibles brechas o inconsistencias en el diseño Recomendaciones de mejora para robustecer el MVP 📥 INFORMACIÓN DE ENTRADA [AQUÍ PEGAR LOS CASOS DE USO] [AQUÍ PEGAR EL CONTEXTO DEL PROYECTO] 📤 FORMATO DE RESPUESTA OBLIGATORIO Responde con la siguiente estructura: 1️⃣ Alcance Funcional del MVP Qué funcionalidades incluye explícitamente Qué procesos cubre de inicio a fin Qué actores participan Qué queda fuera del alcance 2️⃣ Alcance Técnico Arquitectura identificada Componentes principales Tipo de orquestación Gestión de memoria Manejo de errores Persistencia 3️⃣ Objetivos del Sistema 🎯 Estratégicos (Impacto general del proyecto) ⚙️ Operativos (Qué debe lograr técnicamente) 4️⃣ Límites del Sistema Límites funcionales Límites técnicos Límites operativos (iteraciones, validación humana, etc.) 5️⃣ Supuestos Clave Supuestos técnicos Supuestos de usuario Supuestos de infraestructura 6️⃣ Riesgos Identificados Clasificarlos en: Técnicos De calidad del output De escalabilidad De experiencia de usuario De gobernanza/HITL 7️⃣ Métricas de Éxito (KPIs) Definir métricas medibles como: Calidad del itinerario Número promedio de iteraciones Tasa de aprobación humana Tasa de errores de agentes Tiempo total de generación Consistencia entre versiones 8️⃣ Brechas o Inconsistencias Detectadas Identificar posibles puntos débiles en: Flujo iterativo Gestión de memoria Manejo de errores Supervisión humana Persistencia 9️⃣ Recomendaciones de Mejora Priorizar en: Alta prioridad Media prioridad Baja prioridad 🔎 Nivel de profundidad esperado El análisis debe ser: Técnico Crítico Orientado a arquitectura Enfocado en MVP realista Sin explicaciones genéricas Sin repetir literalmente los casos de uso Si detectas ambigüedades, explícitalas como riesgos o supuestos.

---

# 🏗 3️⃣ Diseño y Arquitectura

## 🎯 Objetivo

Diseñar una arquitectura modular, desacoplada, multi‑agente y preparada para producción.

## 🧠 Uso de IA

Se utilizó para:
- Definir estructura backend y frontend
- Diseñar agentes especializados
- Establecer flujo obligatorio del orquestador
- Definir reglas críticas de negocio
- Forzar cumplimiento técnico sin pseudocódigo

---

## 📌 Prompt 3 — Implementación Completa Backend + Frontend
Quiero que implementes un sistema completo dividido en Backend y Frontend, siguiendo una arquitectura modular multi‑agente para búsqueda y análisis de vuelos y alojamientos. No usar pseudocódigo. Código real, ejecutable y modular. Preparado para producción. 🎯 OBJETIVO GENERAL El sistema debe: Recibir datos estructurados para búsqueda de vuelos. Buscar ofertas reales en la web mediante scraping. Si no hay vuelos: Mostrar el mensaje: "No hemos encontrado ofertas con tus requisitos" No ejecutar búsqueda de casas. Si hay vuelos: Mostrar todas las ofertas. Analizar y devolver las 5 mejores calidad-precio. Permitir selección por el usuario (HITL). Luego buscar alojamientos (Airbnb y Booking). Analizar y devolver las 5 mejores opciones. Permitir aprobación final. 🖥 PARTE 1 — BACKEND Implementar con: Python 3.11+ FastAPI Pydantic Async/await httpx o Playwright para scraping Arquitectura modular 📁 Estructura Backend backend/ │ ├── main.py ├── api/ │ └── routes.py │ ├── orchestrator/ │ └── flow.py │ ├── agents/ │ ├── flight_planner.py │ ├── flight_analyst.py │ ├── house_planner.py │ ├── house_analyst.py │ └── documentalist.py │ ├── tools/ │ └── web_scraper.py │ ├── models/ │ ├── flight_models.py │ └── house_models.py │ ├── persistence/ │ └── requirements.txt

✈️ Modelo de Entrada de Vuelos (OBLIGATORIO) NO usar prompt libre. class FlightRequest(BaseModel): origin_airport: str destination_country: str departure_date: date return_date: date passengers: int max_budget: float

🤖 AGENTES BACKEND 1️⃣ FlightPlannerAgent Usa WebScraper. Busca en: Skyscanner Google Flights Kayak Kiwi Expedia Devuelve lista de FlightOffer. Si lista vacía → el orquestador debe terminar flujo.

2️⃣ FlightAnalystAgent Recibe todas las ofertas. Calcula score calidad‑precio. Devuelve máximo 5 mejores.

3️⃣ HousePlannerAgent Se ejecuta solo si hay vuelo seleccionado. Busca en: Airbnb Booking Usa WebScraper. Ajusta a presupuesto restante.

4️⃣ HouseAnalystAgent Evalúa precio, rating, servicios, ubicación. Devuelve Top 5.

5️⃣ DocumentalistAgent Responsable de estructurar la información para frontend. Fases: Mostrar todas las ofertas Mostrar Top 5 seleccionadas Generar respuesta estructurada tipo: {"phase": "all_flights" | "top_flights" | "all_houses" | "top_houses","data": [...]}

🛠 Tool WebScraper Debe: Soportar asincronía Manejar errores Normalizar datos Preparado para Playwright o httpx

🔁 Orquestador Backend Flujo obligatorio:

Recibir FlightRequest
Ejecutar FlightPlanner
Si vacío: devolver mensaje obligatorio
Documentalist → todas las ofertas
FlightAnalyst → Top 5
Documentalist → mostrar Top 5
Esperar selección usuario
Ejecutar HousePlanner
Documentalist → todas casas
HouseAnalyst → Top 5
Documentalist → mostrar Top 5
Esperar aprobación final
❗ Regla Crítica Backend Si no hay vuelos: Devolver exactamente: "No hemos encontrado ofertas con tus requisitos" Y no ejecutar búsqueda de casas.

🌐 PARTE 2 — FRONTEND Implementar con: React o Next.js TypeScript Arquitectura modular Consumo de API REST del backend

📁 Estructura Frontend frontend/ │ ├── pages/ │ ├── index.tsx │ └── results.tsx │ ├── components/ │ ├── FlightForm.tsx │ ├── FlightList.tsx │ ├── HouseList.tsx │ ├── OfferCard.tsx │ └── ApprovalPanel.tsx │ ├── services/ │ └── api.ts │ └── styles/

📝 Formulario de Vuelos Campos obligatorios: Aeropuerto origen País destino Fecha ida Fecha vuelta Pasajeros Presupuesto Validación obligatoria.

🖥 Flujo Frontend Formulario vuelos ↓ POST /flights/search ↓ Mostrar todas las ofertas ↓ Mostrar Top 5 ↓ Usuario selecciona vuelo ↓ POST /houses/search ↓ Mostrar todas casas ↓ Mostrar Top 5 ↓ Usuario aprueba ↓ Mostrar resumen final

🧠 Comportamiento HITL El usuario debe poder: Seleccionar vuelo Rechazar Top 5 Forzar nueva búsqueda Seleccionar casa Aprobar plan final

📦 REQUISITOS GENERALES Código limpio y modular Tipado fuerte Manejo de errores Logging Fácilmente extensible Preparado para Docker Backend y Frontend desacoplados

✅ RESULTADO FINAL ESPERADO El sistema completo debe: Ejecutar backend con: uvicorn main:app --reload

Ejecutar frontend con: npm run dev

Tener flujo completo funcional Manejar correctamente caso sin vuelos Implementar scraping real o estructura preparada para ello No usar pseudocódigo No omitir archivos

---

# 🔍 4️⃣ Validación Arquitectónica

## 🎯 Objetivo

Auditar si la implementación cumple con la arquitectura conceptual definida.

## 🧠 Uso de IA

Se utilizó como revisor técnico para validar coherencia entre:
- Diseño conceptual
- Implementación real
- Separación de responsabilidades
- Modularidad
- Escalabilidad futura

---

## 📌 Prompt 4 — Revisión de Arquitectura
revisa mi codigo y dime si sigue estas indicaciones orientativas que cree:

1️⃣ Visión General de Arquitectura Estilo arquitectónico Arquitectura modular orientada a agentes Orquestación centralizada Separación clara entre: Presentación Lógica multi‑agente Persistencia Servicios externos 🧱 2️⃣ Componentes Principales

Capa de Presentación Responsabilidad: Interacción con el usuario. Web App / API REST Formularios de viaje Visualización del itinerario Edición del plan
API Backend Expone endpoints como: POST /travel-request GET /travel-plan/{id} PUT /travel-plan/{id} POST /travel-plan/{id}/refine
Orquestador de Agentes Es el núcleo del sistema. Responsabilidades: Coordinar el flujo Ejecutar agentes en orden Gestionar iteraciones Activar revisión humana si es necesario Flujo interno: Recibe TravelRequest Ejecuta Agente Analista Ejecuta Agente Planificador Ejecuta Agente Crítico Si hay errores → vuelve a planificador Si es ambiguo → activa HITL Devuelve plan final
Agentes IA 🧠 Agente Analista Interpreta requisitos del usuario Normaliza datos Extrae: Tipo de viaje Nivel de presupuesto Restricciones clave Output: StructuredTravelSpec 🗺 Agente Planificador Genera itinerario por días Asigna: Actividades Tiempos Coste estimado Justifica decisiones Output: TravelPlanDraft 🔎 Agente Crítico Valida: Presupuesto Coherencia temporal Restricciones Detecta conflictos Devuelve: Aprobado Requiere refinamiento Requiere revisión humana Output: ValidationReport 👤 Módulo HITL (Human-in-the-loop) Interfaz para revisor humano Permite: Aprobar Editar Rechazar
Persistencia Base de datos (PostgreSQL o similar): Entidades principales: User TravelRequest StructuredSpec TravelPlan ValidationReport PlanVersion
Servicios Externos (Opcional en MVP) API de clima API de vuelos API de mapas Base de datos de puntos turísticos 🔄 3️⃣ Flujo de Datos Usuario ↓ Frontend ↓ Backend API ↓ Orquestador ↓ [Analista] → [Planificador] → [Crítico] ↑ ↓ Refinamiento ← Validación ↓ HITL (si necesario) ↓ Plan Final ↓ Base de Datos
🧩 4️⃣ Modelo de Dominio Simplificado TravelRequest

id
destination
start_date
end_date
budget
preferences
constraints TravelPlan
id
request_id
days[]
total_cost
justification
status DayPlan
date
activities[] Activity
name
location
estimated_cost
duration ⚙ 5️⃣ Arquitectura Técnica (Ejemplo Tecnológico) Backend Python + FastAPI Motor LLM (OpenAI / local) LangGraph o similar para orquestación Base de Datos PostgreSQL Frontend React / Next.js Infraestructura Docker Despliegue en cloud (Render, AWS, etc.) 📐 6️⃣ Justificación Arquitectónica Decisión Justificación Orquestador central Control del flujo multi‑agente Separación por agentes Modularidad y escalabilidad Validación independiente Mayor robustez Versionado de planes Permite refinamiento iterativo HITL opcional Reduce errores críticos 🚀 7️⃣ Escalabilidad Futura Añadir agente optimizador de costes Añadir motor de recomendación basado en historial Cache semántica Integración con reservas reales Arquitectura basada en eventos ✅ Resultado Con esta arquitectura demuestras: Diseño modular Aplicación clara de sistema multi‑agente Separación de responsabilidades Escalabilidad Control de calidad mediante agente crítico y HITL

---

# 📚 5️⃣ Documentación Técnica

## 🎯 Objetivo

Generar documentación técnica exhaustiva alineada con buenas prácticas de ingeniería.

## 🧠 Uso de IA

Se utilizó para:
- Documentar arquitectura
- Explicar patrones
- Analizar estructuras de datos
- Relacionar diseño técnico con lógica de negocio

---

## 📌 Prompt 5 — Documentación Exhaustiva
Elaborar una documentación exhaustiva de todas las secciones de código proporcionadas, que abarque la arquitectura, las mejores prácticas, los patrones, las estructuras de datos y los análisis de negocio


---

# ✅ Conclusión

Durante el desarrollo del proyecto, la IA fue utilizada estratégicamente en múltiples fases del ciclo de vida del software, demostrando:

- ✅ Uso consciente y estructurado de agentes
- ✅ Análisis crítico previo a implementación
- ✅ Diseño arquitectónico modular
- ✅ Separación clara entre IA y lógica determinista
- ✅ Validación arquitectónica formal
- ✅ Documentación técnica asistida por IA

El sistema final no solo implementa un enfoque multi‑agente, sino que demuestra madurez en el uso de IA dentro del proceso completo de ingeniería de software.
