# Sistemas hibrido de asistencia juridica

## Requisitos

- Python ≥ 3.13 (ver [.python-version](.python-version))
- [uv](https://docs.astral.sh/uv/) para gestionar el entorno y las dependencias

## Uso

```bash
# Instalación de librerías
uv sync

# Renderizar la presentación
uv run python -m manim_slides render main.py presentation

# Presentar
uv run python -m manim_slides present presentation
```