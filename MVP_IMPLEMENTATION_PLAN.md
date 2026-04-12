# MVP Implementation Plan (Actualizado al Código Actual)

Este documento describe el estado real del sistema y el plan necesario para convertirlo en un MVP productivo completo, basado estrictamente en la arquitectura actualmente implementada en `backend/graph`.

---

# ✅ 1. Estado Actual Implementado

## Arquitectura Base

Actualmente el sistema ya dispone de:

- ✅ FastAPI (`backend/api/app.py`)
- ✅ Arquitectura basada en grafo
- ✅ Graph Builder (`backend/graph/graph_builder.py`)
- ✅ State compartido (`backend/graph/state.py`)
- ✅ Nodos desacoplados (`backend/graph/nodes.py`)
- ✅ Agentes definidos en `backend/graph/agents.py`
- ✅ Tools desacopladas (`backend/graph/tools.py`)
- ✅ Lógica de dominio en `backend/domain/*`
- ✅ Modelos tipados con Pydantic (`backend/models/*`)
- ✅ Cliente LLM encapsulado (`backend/llm/client.py`)

---

# ✅ 2. Flujo MVP Actual

El flujo actual del sistema es:

```
Request usuario
    ↓
FastAPI
    ↓
Construcción de State inicial
    ↓
Graph Builder
    ↓
Nodo Agente
    ↓
Invocación Tool (si aplica)
    ↓
Actualización State
    ↓
Resultado final
```

El núcleo multi-agente ya está correctamente implementado.

---

# ❌ 3. Gaps Reales para MVP Productivo

## 3.1 Persistencia

Actualmente el sistema es stateless.

Falta implementar:

- PostgreSQL
- SQLAlchemy (o equivalente)
- Tablas mínimas:
  - users
  - travel_requests
  - selected_flight
  - selected_house
  - final_document
  - execution_logs
- Versionado de planes

---

## 3.2 Gestión de Sesiones

Actualmente:
- No existe gestión persistente de sesión.
- El state vive únicamente durante la ejecución del grafo.

Se requiere:
- Asociar ejecución a user_id
- Persistir estado final
- Posibilidad de recuperar ejecución previa

---

## 3.3 API Extendida

Actualmente existe API básica.

Para MVP completo debería incluir:

- POST /travel-request
- GET /travel-plan/{id}
- POST /select-flight
- POST /select-house
- GET /execution/{id}
- GET /health

---

## 3.4 Robustez Infraestructura

Falta:

- Dockerfile backend
- Dockerfile frontend
- docker-compose
- Configuración producción
- Logging estructurado
- Manejo robusto de errores en scraping
- Timeout + retry pattern

---

# 🎯 4. MVP Target Realista

Para considerar el sistema como MVP productivo se deben cumplir:

1. Persistencia PostgreSQL
2. Gestión de usuarios básica
3. Logging estructurado por ejecución
4. Manejo robusto de errores scraping
5. Dockerización completa
6. Validación fuerte de inputs API

---

# 📌 5. Roadmap Actualizado

## Fase 1 – Persistencia
- Integrar SQLAlchemy
- Crear modelos ORM
- Guardar resultados finales del grafo
- Asociar ejecución a usuario

## Fase 2 – API Extendida
- Implementar endpoints CRUD
- Endpoint selección vuelo
- Endpoint selección alojamiento
- Endpoint recuperación ejecución

## Fase 3 – Infraestructura
- Docker backend
- Docker frontend
- docker-compose
- Variables entorno seguras

## Fase 4 – Observabilidad
- Logging estructurado
- Correlation ID por ejecución
- Métricas básicas
- Manejo errores scraping robusto

---

# ✅ 6. Conclusión

El núcleo multi-agente y la arquitectura basada en grafo ya están correctamente implementados y bien diseñados.

El sistema actual es sólido a nivel arquitectónico.

Para convertirlo en MVP productivo faltan principalmente:

- Persistencia
- Infraestructura
- Observabilidad
- Robustez operativa

La base técnica ya está correctamente construida.
