# AgenciaViajes - Plan Real Basado en el Código Actual

Este documento describe el proyecto según la implementación real existente en el repositorio.

---

# ✅ Arquitectura Actual Consolidada

```
Frontend (React + Vite)
        ↓
FastAPI (backend/api/app.py)
        ↓
Graph Builder
        ↓
Nodes (Agente / Tool / Control)
        ↓
Domain Layer
        ↓
Tools (Web Scraper)
```

No existe ya separación entre “MVP antiguo” y “nuevo sistema”.  
El proyecto actual está consolidado en una única arquitectura basada en grafo.

---

# ✅ Backend Structure Real

```
backend/
├── api/
│   └── app.py
├── graph/
│   ├── graph_builder.py
│   ├── nodes.py
│   ├── state.py
│   ├── agents.py
│   └── tools.py
├── domain/
│   ├── flight_planner.py
│   ├── flight_analyst.py
│   ├── house_planner.py
│   ├── house_analyst.py
│   └── documentalist.py
├── models/
│   ├── flight_models.py
│   └── house_models.py
├── tools/
│   └── web_scraper.py
├── llm/
│   └── client.py
```

---

# ✅ Funcionamiento Actual

## Flujo simplificado

1. Usuario envía request
2. FastAPI construye state inicial
3. Graph Builder crea flujo
4. Nodo agente ejecuta LLM
5. Si el LLM decide → se invoca tool
6. Tool ejecuta lógica dominio / scraping
7. State se actualiza
8. Se produce resultado final

---

# ✅ Agentes Implementados

En dominio existen:

- FlightPlanner
- FlightAnalyst
- HousePlanner
- HouseAnalyst
- Documentalist

El sistema utiliza patrón:

Planner → Analyst → Selección → Documentalist

---

# ✅ Web Scraping

Ubicación:
```
backend/tools/web_scraper.py
```

Responsabilidad:
- Buscar vuelos
- Buscar alojamientos
- Devolver resultados estructurados

Actualmente no incluye:
- Retry robusto
- Circuit breaker
- Rate limiting avanzado

---

# ❌ Elementos No Implementados

## Persistencia
No existe:
- PostgreSQL
- ORM
- Versionado de planes
- Historial de ejecución

## Infraestructura
No existe:
- Dockerfile
- docker-compose
- Configuración despliegue
- CI/CD

## Observabilidad
No existe:
- Logging estructurado por ejecución
- Métricas
- Trazabilidad LLM detallada

---

# 🎯 Plan Realista de Evolución

## Fase 1 – Robustez Scraping
- Timeouts explícitos
- Manejo de excepciones
- Retry pattern
- Logging detallado

## Fase 2 – Persistencia
- SQLAlchemy
- Tablas:
  - users
  - executions
  - selected_flight
  - selected_house
  - final_document

## Fase 3 – API Extendida
- Endpoint selección vuelo
- Endpoint selección alojamiento
- Recuperación ejecución previa

## Fase 4 – Infraestructura
- Docker backend
- Docker frontend
- docker-compose
- Variables entorno seguras

---

# ✅ Estado Actual del Proyecto

El sistema actual es:

- Arquitectura moderna basada en grafo
- Separación limpia dominio / infraestructura
- Tool calling bien implementado
- Modelo extensible
- Preparado para escalar

No es ya un “proyecto de transformación”, sino un sistema consolidado que requiere:

- Infraestructura
- Persistencia
- Observabilidad

para convertirse en production-ready.

---

# ✅ Conclusión

El proyecto actual ya implementa correctamente:

- Orquestación basada en grafo
- Multi-agente especializado
- Tool execution desacoplada
- Dominio limpio

La evolución futura debe centrarse en:

- Persistencia
- Infraestructura
- Robustez operacional

La base arquitectónica está correctamente construida y es extensible.
