# 📊 Análisis de Arquitectura - Sistema AgenciaViajes (Estado Actual del Código)

## Resumen Ejecutivo

Este documento refleja el **estado real actual del repositorio** según la estructura presente en:

- `backend/graph/*`
- `backend/domain/*`
- `backend/models/*`
- `backend/tools/*`
- `backend/api/app.py`
- `frontend/*`

**Fecha de revisión:** 12 abril 2026  
**Estado actual:** ✅ Arquitectura basada en grafo con agentes + tools (sin doble sistema MVP)

---

# 1️⃣ Visión General Real del Sistema

Actualmente el sistema NO mantiene dos arquitecturas paralelas (MVP + nuevo).  
El código consolidado implementa:

> Arquitectura basada en grafo de ejecución + agentes especializados + tools determinísticas.

Estructura principal:

```
Frontend (React + Vite)
        ↓
FastAPI (backend/api/app.py)
        ↓
Graph Builder
        ↓
Nodes (Agente / Tool / Control)
        ↓
Domain + Tools
```

---

# 2️⃣ Arquitectura Backend Actual

## 2.1 Capa API

Archivo:
```
backend/api/app.py
```

Responsabilidades reales:
- Exposición de endpoints FastAPI
- Construcción de estado inicial
- Ejecución del grafo
- Devolución del resultado final

✅ No existe ya un `travel_itinerary_mvp/` activo en esta arquitectura.
✅ El sistema actual es único y basado en grafo.

---

## 2.2 Orquestación (Graph-Based)

Archivos:

```
backend/graph/
    graph_builder.py
    nodes.py
    state.py
    agents.py
    tools.py
```

El sistema utiliza:

- State compartido
- Nodos funcionales
- Transiciones explícitas
- Control determinístico del flujo

No se utiliza LangGraph directamente, pero el patrón es equivalente.

---

## 2.3 State

Archivo:
```
backend/graph/state.py
```

Responsabilidades:
- Mantener contexto de ejecución
- Almacenar resultados intermedios
- Gestionar selección de vuelo y alojamiento
- Persistir outputs parciales

El state actúa como memoria transaccional del grafo.

✅ Separación clara entre control y lógica.

---

## 2.4 Agentes

Archivo:
```
backend/graph/agents.py
```

El sistema implementa agentes que:

- Construyen prompts
- Invocan LLM vía `backend/llm/client.py`
- Deciden llamadas a tools
- Generan respuestas finales

Separación clara:

| Componente | Rol |
|------------|------|
| LLM | Razonamiento |
| Tool | Ejecución determinística |
| Grafo | Control |

---

## 2.5 Dominio

Directorio:
```
backend/domain/
```

Contiene:

- flight_planner.py
- flight_analyst.py
- house_planner.py
- house_analyst.py
- documentalist.py

✅ El dominio NO depende del LLM.
✅ El dominio NO conoce el grafo.
✅ Arquitectura limpia (Clean Architecture).

---

## 2.6 Tools

Archivos relevantes:

```
backend/graph/tools.py
backend/tools/web_scraper.py
```

Las tools:

- Conectan con lógica de dominio
- Ejecutan scraping
- Devuelven resultados estructurados
- Son invocadas por el agente vía grafo

✅ Correcta separación ejecución / razonamiento.

---

# 3️⃣ Modelo de Datos

Ubicación:

```
backend/models/
```

Incluye:

- flight_models.py
- house_models.py

Uso de Pydantic para:

- Validación
- Tipado fuerte
- Contratos claros

✅ Diseño consistente con arquitectura moderna.

---

# 4️⃣ Frontend

Estructura real:

```
frontend/
  src/
    App.jsx
    main.jsx
    styles.css
```

Frontend básico React + Vite.

✅ Permite integración con backend.
⚠️ No implementa aún flujos avanzados de selección compleja.

---

# 5️⃣ Persistencia

Estado actual:

❌ No existe PostgreSQL.
❌ No existe ORM.
❌ No existe versionado de planes.

El sistema es actualmente stateless por ejecución.

Esto simplifica el MVP pero limita:

- Historial
- Versionado
- Auditoría
- Escalabilidad empresarial

---

# 6️⃣ Evaluación Arquitectónica Actual

| Área | Estado |
|------|--------|
| Arquitectura por agentes | ✅ Sólida |
| Orquestación por grafo | ✅ Correcta |
| Separación dominio | ✅ Limpia |
| Tool calling | ✅ Correcto |
| Persistencia | ❌ No implementada |
| Infraestructura | ⚠️ Básica |
| Frontend | ⚠️ MVP simple |

---

# 7️⃣ Puntuación Actualizada

| Criterio | Puntuación |
|----------|------------|
| Diseño de agentes | 9/10 |
| Orquestación | 9/10 |
| Dominio | 9/10 |
| Persistencia | 3/10 |
| Infraestructura | 6/10 |
| Frontend | 6/10 |

### ✅ Puntuación Global Realista: 8/10

---

# 8️⃣ Conclusión Actual

El sistema actual es:

> Arquitectura moderna basada en grafo + agentes especializados + tools determinísticas.

No es ya un doble sistema MVP / nuevo sistema.  
Está consolidado en una única arquitectura coherente.

Las mejoras prioritarias reales son:

1. Persistencia real (PostgreSQL)
2. Observabilidad y logging avanzado
3. Manejo robusto de errores en scraping
4. Dockerización

El núcleo arquitectónico es sólido, extensible y alineado con patrones modernos de sistemas de agentes productivos.
