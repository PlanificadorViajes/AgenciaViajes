# Travel Itinerary MVP System

🌍 Sistema de generación iterativa de itinerarios de viaje utilizando arquitectura basada en agentes (Generator + Critic) con orquestador con estado.

## 🎯 Descripción

Este sistema permite generar, revisar y refinar planes complejos iterativamente (viajes, agendas, proyectos o itinerarios), utilizando una arquitectura modular y extensible basada en dos agentes especializados:

- **Generator Agent**: Crea propuestas estructuradas de itinerarios
- **Critic Agent**: Evalúa y proporciona feedback para mejoras
- **Orchestrator**: Coordina el proceso iterativo hasta obtener un plan aprobado

## 🏗️ Arquitectura

```
travel_itinerary_mvp/
│
├── main.py                    # Punto de entrada principal
│
├── config/
│   ├── settings.py            # Configuración del sistema
│   └── prompts/
│       ├── generator.txt      # Prompts del agente generador
│       └── critic.txt         # Prompts del agente crítico
│
├── agents/
│   ├── generator.py           # Agente generador de planes
│   └── critic.py              # Agente crítico evaluador
│
├── graph/
│   ├── state.py               # Gestión de estado del proceso
│   └── orchestrator.py        # Orquestador del flujo de trabajo
│
├── memory/
│   └── session_store.py       # Almacenamiento de sesiones
│
├── persistence/
│   └── repository.py          # Persistencia de datos
│
├── data/                      # Datos generados (auto-creado)
├── logs/                      # Archivos de log (auto-creado)
└── requirements.txt           # Dependencias del proyecto
```

## 🚀 Instalación y Uso

### Requisitos Previos

- Python 3.11+
- pip o poetry para gestión de dependencias

### Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone <repository-url>
   cd travel_itinerary_mvp
   ```

2. **Crear entorno virtual:**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/macOS
   source venv/bin/activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

### Ejecución

```bash
# Desde la raíz del proyecto
python -m travel_itinerary_mvp.main

# O alternativamente
cd travel_itinerary_mvp
python main.py
```

### Ejemplo de Uso

```
🌍 Welcome to Travel Itinerary Generator!
Please describe your travel requirements:
(Example: '7 days trip to Japan with medium budget')

> 7 días en Japón con presupuesto medio

🔄 Processing your request: '7 días en Japón con presupuesto medio'
This may take a few moments...
```

## 🔄 Flujo de Trabajo

1. **Input del Usuario**: Descripción de requisitos de viaje
2. **Generator**: Crea propuesta inicial estructurada
3. **Critic**: Evalúa el plan según criterios de calidad:
   - Coherencia y consistencia
   - Factibilidad y presupuesto
   - Optimización temporal
   - Gestión de riesgos
   - Nivel de detalle
4. **Decisión**: 
   - ✅ **Aprobado** → Guardar resultado
   - ❌ **Rechazado** → Refinar con feedback y repetir
5. **Persistencia**: Almacenamiento en `data/itineraries.json`

## 🧠 Componentes Principales

### Generator Agent
- Genera planes estructurados en formato JSON
- Acepta objetivos, restricciones y feedback
- Produce planes detallados con justificación y estimaciones

### Critic Agent
- Evalúa planes según criterios definidos
- Proporciona puntuación (0-10) y feedback específico
- Identifica problemas y sugiere mejoras

### Orchestrator
- Controla el flujo iterativo del proceso
- Gestiona límites máximos de iteraciones
- Mantiene estado y registra logs

### State Management
- Seguimiento completo del estado de la sesión
- Historial de iteraciones y cambios
- Persistencia entre ejecuciones

## 🛠️ Configuración

El archivo `config/settings.py` permite personalizar:

- Límites máximos de iteraciones
- Criterios de aprobación
- Configuración de logging
- Rutas de datos y archivos

Los prompts pueden modificarse en:
- `config/prompts/generator.txt`
- `config/prompts/critic.txt`

## 📊 Estructura de Datos

### Plan State
```python
class PlanState:
    user_input: str          # Entrada del usuario
    current_plan: dict       # Plan actual
    critic_feedback: dict    # Feedback del crítico
    iteration: int           # Número de iteración
    approved: bool           # Estado de aprobación
    session_id: str          # Identificador de sesión
```

### Formato de Salida del Critic
```json
{
  "score": 8.5,
  "issues": ["Lista de problemas identificados"],
  "improvements": ["Lista de mejoras sugeridas"],
  "approved": true
}
```

## 🔧 Extensibilidad

El sistema está diseñado para ser fácilmente extensible:

### Añadir Nuevos Agentes
1. Crear nueva clase en `agents/`
2. Implementar interfaz común
3. Registrar en el orquestador

### Integración con LLMs
- Preparado para integración con OpenAI, Anthropic, etc.
- Interfaces modulares para diferentes proveedores

### Nuevos Tipos de Planes
- Extensible a agendas, proyectos, eventos
- Modificación de prompts y criterios de evaluación

## 📝 Logs y Debugging

- Logging estructurado en `logs/`
- Diferentes niveles de verbosidad
- Trazabilidad completa del proceso

## 🧪 Desarrollo

### Estructura para Testing
```bash
# Instalar dependencias de desarrollo
pip install pytest pytest-cov black flake8 mypy

# Ejecutar tests
pytest

# Verificar tipos
mypy travel_itinerary_mvp/

# Formatear código
black travel_itinerary_mvp/
```

### Pre-commit Hooks
Configuración recomendada para desarrollo colaborativo.

## 🤝 Contribución

1. Fork del proyecto
2. Crear rama de feature (`git checkout -b feature/AmazingFeature`)
3. Commit de cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📋 Roadmap

- [ ] Integración con APIs de LLM reales
- [ ] Interface web con FastAPI
- [ ] Soporte para múltiples idiomas
- [ ] Sistema de plugins para agentes
- [ ] Integración con APIs de viajes
- [ ] Dashboard de métricas y analytics

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🆘 Soporte

Para reportar bugs o solicitar features, por favor crear un issue en el repositorio de GitHub.

---

**Versión**: 1.0.0  
**Autor**: Desarrollado para arquitectura basada en agentes  
**Estado**: MVP funcional listo para extensión
