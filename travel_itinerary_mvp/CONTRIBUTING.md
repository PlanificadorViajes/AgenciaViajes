# Guía de Contribución

¡Gracias por tu interés en contribuir al Travel Itinerary MVP System! Esta guía te ayudará a empezar.

## 🤝 Código de Conducta

Este proyecto adhiere a un código de conducta. Al participar, se espera que mantengas este estándar.

## 🚀 Cómo Contribuir

### Reportar Bugs

1. **Busca primero** en los issues existentes para evitar duplicados
2. **Usa la plantilla** de issue para bugs
3. **Incluye información detallada**:
   - Versión de Python
   - Sistema operativo
   - Pasos para reproducir
   - Comportamiento esperado vs actual
   - Logs relevantes

### Sugerir Mejoras

1. **Busca issues similares** antes de crear uno nuevo
2. **Usa la plantilla** de feature request
3. **Describe claramente**:
   - El problema que resuelve
   - La solución propuesta
   - Alternativas consideradas

### Pull Requests

1. **Fork** el repositorio
2. **Crea una rama** desde `main`:
   ```bash
   git checkout -b feature/nombre-descriptivo
   ```
3. **Implementa** tu cambio siguiendo las convenciones
4. **Añade tests** si es aplicable
5. **Actualiza documentación** si es necesario
6. **Commit** con mensajes descriptivos
7. **Push** y crea el Pull Request

## 📋 Estándares de Desarrollo

### Convenciones de Código

- **PEP 8** para estilo de Python
- **Type hints** obligatorios
- **Docstrings** en formato Google/NumPy
- **Nombres descriptivos** para variables y funciones

### Estructura de Commits

Usa [Conventional Commits](https://www.conventionalcommits.org/):

```
tipo(alcance): descripción

feat(agents): añadir nuevo agente de validación
fix(orchestrator): corregir manejo de errores
docs(readme): actualizar instrucciones de instalación
style(format): aplicar formato con black
refactor(state): simplificar gestión de estado
test(critic): añadir tests para evaluación
chore(deps): actualizar dependencias
```

### Testing

- **Cobertura mínima**: 80%
- **Tests unitarios** para lógica de negocio
- **Tests de integración** para flujos completos
- **Mocks** para dependencias externas

```bash
# Ejecutar tests
pytest

# Con cobertura
pytest --cov=travel_itinerary_mvp

# Solo tests rápidos
pytest -m "not slow"
```

### Linting y Formateo

```bash
# Formateo automático
black travel_itinerary_mvp/

# Verificar estilo
flake8 travel_itinerary_mvp/

# Verificar tipos
mypy travel_itinerary_mvp/

# Imports ordenados
isort travel_itinerary_mvp/
```

## 🏗️ Arquitectura del Proyecto

### Principios de Diseño

- **Separación de responsabilidades**
- **Inyección de dependencias**
- **Principio abierto/cerrado**
- **Single Responsibility Principle**

### Patrones Utilizados

- **Agent Pattern** para comportamientos especializados
- **State Pattern** para gestión de estados
- **Repository Pattern** para persistencia
- **Factory Pattern** para creación de objetos

### Estructura de Módulos

```
travel_itinerary_mvp/
├── agents/          # Agentes especializados
├── config/          # Configuración y prompts
├── graph/           # Orquestación y estado
├── memory/          # Gestión de memoria/sesiones
└── persistence/     # Capa de datos
```

## 🔧 Setup de Desarrollo

### Requisitos

- Python 3.11+
- pip o poetry
- Git

### Configuración Local

1. **Clona tu fork**:
   ```bash
   git clone https://github.com/tu-usuario/travel_itinerary_mvp.git
   cd travel_itinerary_mvp
   ```

2. **Configura upstream**:
   ```bash
   git remote add upstream https://github.com/org-original/travel_itinerary_mvp.git
   ```

3. **Crea entorno virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # o
   venv\Scripts\activate     # Windows
   ```

4. **Instala dependencias**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

5. **Configura pre-commit hooks**:
   ```bash
   pre-commit install
   ```

### Variables de Entorno

Crea un archivo `.env` para desarrollo local:

```bash
# .env
PYTHONPATH=.
LOG_LEVEL=DEBUG
MAX_ITERATIONS=5
```

## 📝 Documentación

### Docstrings

```python
def ejemplo_funcion(param1: str, param2: int) -> bool:
    """Descripción breve de la función.
    
    Args:
        param1: Descripción del parámetro 1
        param2: Descripción del parámetro 2
        
    Returns:
        Descripción del valor de retorno
        
    Raises:
        ValueError: Cuándo se produce esta excepción
        
    Example:
        >>> ejemplo_funcion("test", 42)
        True
    """
    pass
```

### README Updates

- Mantener ejemplos actualizados
- Documentar nuevas funcionalidades
- Actualizar roadmap

## 🧪 Guidelines de Testing

### Estructura de Tests

```
tests/
├── unit/
│   ├── agents/
│   ├── graph/
│   └── persistence/
├── integration/
└── fixtures/
```

### Convenciones

- Archivos: `test_*.py`
- Clases: `Test*`
- Métodos: `test_*`
- Fixtures en `conftest.py`

### Ejemplo de Test

```python
import pytest
from travel_itinerary_mvp.agents.generator import GeneratorAgent

class TestGeneratorAgent:
    @pytest.fixture
    def generator(self):
        return GeneratorAgent()
    
    def test_generate_plan_success(self, generator):
        # Arrange
        user_input = "5 días en Barcelona"
        
        # Act
        result = generator.generate_plan(user_input)
        
        # Assert
        assert result is not None
        assert "Barcelona" in result["destination"]
```

## 🚦 Pipeline de CI/CD

### GitHub Actions

El proyecto usa GitHub Actions para:

- **Linting** (flake8, mypy)
- **Testing** (pytest con cobertura)
- **Formateo** (black, isort)
- **Security** (bandit, safety)

### Branch Protection

- `main` protegida
- Requiere PR reviews
- CI debe pasar
- Branch actualizada

## 📋 Checklist de PR

Antes de crear tu Pull Request:

- [ ] Tests pasan localmente
- [ ] Código formateado con black
- [ ] Sin errores de linting
- [ ] Documentación actualizada
- [ ] Changelog actualizado (si aplica)
- [ ] Type hints añadidos
- [ ] Tests añadidos para nueva funcionalidad

## 🎯 Areas de Contribución

### Prioritarias

- [ ] Integración con LLM APIs reales
- [ ] Mejora del sistema de evaluación
- [ ] Tests de integración
- [ ] Performance optimizations

### Funcionalidades Futuras

- [ ] Interface web
- [ ] Soporte multi-idioma
- [ ] Plugins para agentes
- [ ] Métricas y analytics

### Documentación

- [ ] Tutoriales paso a paso
- [ ] Guías de arquitectura
- [ ] Videos explicativos
- [ ] FAQ

## ❓ Obtener Ayuda

- **Issues**: Para bugs y features
- **Discussions**: Para preguntas generales
- **Discord/Slack**: Para chat en tiempo real (si disponible)

## 📚 Recursos Adicionales

- [Python Style Guide](https://pep8.org/)
- [Type Hints Cheat Sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)
- [pytest Documentation](https://docs.pytest.org/)
- [Agent-Based Architecture](https://en.wikipedia.org/wiki/Agent-based_model)

---

¡Gracias por contribuir! 🙏
