# 🌍 DevAgents Lab – Planificador Inteligente de Viajes  
## Propuesta 4: Sistema Multi‑Agente con LangGraph  

---

## 📌 Descripción del Proyecto  

Este proyecto consiste en el desarrollo de un **MVP de un Planificador Inteligente de Viajes**, implementado como un **sistema multi‑agente orquestado con LangGraph**.  

El sistema es capaz de:  
- Generar itinerarios personalizados  
- Criticar propuestas automáticamente  
- Refinar planes de forma iterativa  
- Incorporar un mecanismo **Human‑In‑The‑Loop (HITL)** para validación antes de entregar la versión final  

---

## 🎯 Problema a Resolver  

Los usuarios desean organizar viajes optimizados según:  

- 📍 **Destino**  
- 📅 **Fechas**  
- 💰 **Presupuesto**  
- 🎨 **Intereses** (cultura, gastronomía, naturaleza, ocio, etc.)  
- ⏳ **Restricciones** (tiempo disponible, transporte, horarios)  

El sistema debe:  
- Generar un plan de viaje coherente y estructurado  
- Justificar las decisiones tomadas  
- Detectar inconsistencias o mejoras posibles  
- Permitir revisión humana antes de la versión final  

---

## 🧠 Enfoque Multi‑Agente  

El sistema está compuesto por múltiples agentes especializados que colaboran entre sí:  

### 1️⃣ Agente Planificador  
- Genera un itinerario inicial basado en las preferencias del usuario  
- Distribuye actividades por día  
- Optimiza tiempo y presupuesto  

### 2️⃣ Agente Crítico  
- Evalúa coherencia, viabilidad y calidad del itinerario  
- Detecta conflictos de horario o sobrecarga de actividades  
- Sugiere mejoras o ajustes  

### 3️⃣ Agente Refinador  
- Aplica mejoras sugeridas  
- Ajusta el plan respetando restricciones  
- Produce una versión optimizada  

### 4️⃣ Supervisión Humana (HITL)  
- Revisión del plan generado  
- Posibilidad de feedback manual  
- Aprobación antes de entregar el resultado final  

---

## 🔄 Flujo del Sistema (LangGraph)  

Usuario  
↓  
Planificador  
↓  
Crítico  
↓  
Refinador  
↓  
HITL  
↓  
Itinerario Final  

---

## 🏗️ Arquitectura  

- **Framework de orquestación:** LangGraph  
- **Modelo(s) LLM:** (ej. OpenAI GPT)  
- **Estrategia:** Agent-based workflow  
- **Supervisión:** Human‑In‑The‑Loop  
- **Enfoque:** Modular, escalable y extensible  

---

## 🚀 Objetivos del MVP  

✅ Generar itinerarios personalizados  
✅ Implementar flujo multi‑agente real  
✅ Integrar crítica automática  
✅ Incorporar intervención humana  
✅ Justificar decisiones del sistema  

---

## 📦 Posibles Extensiones Futuras  

- Integración con APIs reales (Google Maps, Skyscanner, Booking)  
- Optimización avanzada de rutas  
- Estimación dinámica de costos  
- Perfilado de usuario persistente  
- Interfaz web interactiva  

---

## 📊 Ejemplo de Input  

```json
{
  "destino": "Roma",
  "fechas": "10-15 Junio 2026",
  "presupuesto": "1500 EUR",
  "intereses": ["historia", "gastronomía", "arte"],
  "restricciones": ["no más de 3 actividades intensivas por día"]
}
```text

---

## 📄 Ejemplo de Output Esperado  

- Itinerario día por día  
- Justificación de selección de actividades  
- Ajuste al presupuesto estimado  
- Explicación de optimización de tiempos  

---

## 🧪 Estado del Proyecto  

🚧 MVP en desarrollo  
📌 Enfoque académico / experimental (DevAgents Lab)  
🧩 Orientado a aprendizaje de sistemas multi‑agente  

---

## 🏁 Conclusión  

Este proyecto explora cómo los **sistemas multi‑agente** pueden colaborar para resolver problemas complejos de planificación, combinando generación creativa, evaluación crítica y supervisión humana.  

El resultado es un planificador **más robusto, transparente y adaptable** que un sistema monolítico tradicional.  



