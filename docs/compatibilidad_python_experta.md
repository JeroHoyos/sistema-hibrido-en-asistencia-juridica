# Nota Técnica: Compatibilidad de Python y Experta (Sistema Experto)

**Fecha:** 2026-09-09  
**Autor / Rama:** `feature/junior-florez`  


---

## 1. Contexto

El repositorio base fue inicializado con **Python 3.13** (`.python-version` y `pyproject.toml`).

La biblioteca requerida para el componente de IA Clásica (Sistemas Basados en Reglas) es **`experta==1.9.4`**.

## 2. Incompatibilidad Identificada

`experta` es una biblioteca madura de producción académica cuyo núcleo depende de estructuras de introspección y colecciones de Python anteriores a la versión 3.10 / 3.12:
1. **`collections.Mapping` vs `collections.abc.Mapping`:** Python 3.10 eliminó los alias de colecciones abstractas dentro del módulo directo `collections`.
2. **`inspect.getargspec`:** Eliminado formalmente en Python 3.11+.

Al intentar instalar y ejecutar `experta` directamente bajo un runtime de Python 3.13, se producen errores en tiempo de importación (`ImportError: cannot import name 'Mapping' from 'collections'`).

## 3. Alternativas Propuestas para el Equipo

1. **Opción A (Recomendada): Configurar el entorno virtual del proyecto con Python 3.10 o 3.11:**
   - Si se usa `uv`:
     ```bash
     uv venv --python 3.10
     ```
   - Si se usa `conda` o `pyenv`:
     ```bash
     conda create -n practica-ia python=3.10
     conda activate practica-ia
     ```
   - Ajustar `.python-version` a `3.10` y en `pyproject.toml`:
     ```toml
     requires-python = ">=3.10,<3.12"
     ```

2. **Opción B: Usar parche de compatibilidad en tiempo de ejecución:**
   - En el punto de entrada o primer notebook/script, inyectar el parche antes de importar `experta`:
     ```python
     import collections
     import collections.abc
     collections.Mapping = collections.abc.Mapping
     collections.MutableMapping = collections.abc.MutableMapping
     collections.Sequence = collections.abc.Sequence
     ```
   *(Nota: Esta opción puede funcionar para prototipos pero puede presentar fallos secundarios en motores de inferencia complejos).*

---

## 4. Próximo Paso en Equipo
- Acordar en la próxima reunión qué versión de Python estandarizaremos para los entornos virtuales de todos los integrantes.
