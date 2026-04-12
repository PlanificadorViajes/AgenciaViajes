# Análisis de Tools del Sistema de Agentes

## 1. Visión General

El sistema implementa un enfoque basado en agentes orquestados mediante un grafo de ejecución.  
Las **tools** representan las capacidades externas o funcionales que los agentes pueden invocar para ejecutar tareas específicas.

Se encuentran principalmente en:

- `backend/graph/tools.py`
- `backend/tools/web_scraper.py`

Las tools actúan como **puntos de integración entre el razonamiento del agente (LLM) y la ejecución determinística del backend**.

---

# 2. Rol Arquitectónico de las Tools

En este sistema:

- El **LLM decide qué hacer**
- Las **tools ejecutan acciones concretas**
- El **grafo controla el flujo**
- El **state mantiene el contexto**

Las tools permiten:

- Acceso a información estructurada
- Llamadas a lógica de dominio
- Integración con fuentes externas
- Transformaciones determinísticas

Esto sigue el patrón moderno de:

> LLM + Tool Calling + Orquestación por Grafo

---

# 3. backend/graph/tools.py

## 3.1 Responsabilidad

Este módulo define las tools que el grafo expone a los agentes.  
Funciona como una capa adaptadora entre:

- Dominio (`backend/domain/*`)
- Modelos (`backend/models/*`)
- Infraestructura externa

## 3.2 Tipología de Tools Identificadas

### 1️⃣ Tools de planificación
Invocan lógica del dominio:

- Flight planner
- House planner

Estas tools:
- No contienen lógica compleja
- Delegan al dominio
- Transforman resultados a formatos esperados por el agente

✅ Buena separación de responsabilidades.

---

### 2️⃣ Tools de análisis
Relacionadas con:

- Flight analyst
- House analyst
- Documentalist

Se usan cuando el agente necesita:

- Evaluar opciones
- Comparar resultados
- Generar análisis estructurado

---

### 3️⃣ Tools de integración externa
Principalmente:

- `web_scraper.py`

Responsables de:
- Obtener datos externos
- Transformarlos a modelos internos

⚠️ Riesgo identificado:
Si no se controla adecuadamente:
- Timeouts
- Manejo de errores
- Sanitización de datos

Puede afectar la estabilidad del sistema.

---

# 4. backend/tools/web_scraper.py

## 4.1 Función

Permite obtener información externa (web scraping).

Rol arquitectónico:
- Tool puramente infraestructura
- No contiene lógica de negocio
- Debe permanecer desacoplada del dominio

## 4.2 Riesgos Técnicos

- Fragilidad ante cambios de HTML
- Dependencia de disponibilidad externa
- Latencia variable
- Posibles bloqueos

## 4.3 Recomendaciones

- Añadir timeouts explícitos
- Manejo robusto de excepciones
- Logging estructurado
- Circuit breaker pattern (opcional en evolución futura)

---

# 5. Flujo de Ejecución de una Tool

1. Usuario realiza petición
2. Se construye estado inicial
3. Grafo inicia ejecución
4. Nodo agente invoca LLM
5. LLM decide llamar una tool
6. Tool ejecuta lógica determinística
7. Resultado se inyecta en el estado
8. El grafo continúa

Este modelo garantiza:

- Control determinístico
- Observabilidad
- Modularidad

---

# 6. Evaluación Arquitectónica

## Fortalezas

✅ Separación dominio / infraestructura  
✅ Bajo acoplamiento  
✅ Extensibilidad alta  
✅ Compatible con múltiples LLMs  

## Debilidades

⚠️ Posible falta de validación de inputs  
⚠️ Gestión de errores distribuida  
⚠️ No se observa mecanismo de retry centralizado  

---

# 7. Nivel de Madurez

Arquitectura alineada con:

- LangGraph-style orchestration
- Tool-based AI agents
- Clean Architecture principles

Nivel estimado:  
**Intermedio-Avanzado**

Permite escalar hacia:

- Multi-agente colaborativo
- Memoria persistente
- Observabilidad avanzada
- Tool routing dinámico

---

# 8. Conclusión

Las tools están correctamente posicionadas como:

> Capa de ejecución determinística controlada por razonamiento probabilístico.

El diseño es coherente, modular y extensible.

No se detectan violaciones graves de arquitectura, aunque existen oportunidades claras de robustecimiento en infraestructura externa.
