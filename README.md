# Sistema Híbrido en Asistencia Jurídica

Proyecto práctico que integra tres paradigmas clásicos de la Inteligencia Artificial: **Sistemas Expertos**, **Lógica Difusa** y **Ontologías con Razonamiento Semántico**, aplicado al dominio de la asesoría y toma de decisiones jurídicas.

**Curso:** Introducción a la Inteligencia Artificial – 3010476 (UNAL Medellín)  
**Profesor:** Jaime Alberto Guzmán Luna  

---

## 🏛️ Arquitectura Modular del Proyecto

Para permitir el desarrollo colaborativo en Git sin colisiones en notebooks, el código fuente está modularizado en `src/`:

```text
sistema-hibrido-en-asistencia-juridica/
├── data/                               # Archivos Turtle (.ttl) y grafos de conocimiento
├── docs/                               # Documentos de diseño, notas técnicas y contratos
│   ├── compatibilidad_python_experta.md
│   └── arquitectura_y_contratos.md
├── src/                                # Código fuente modular del sistema
│   ├── ontologia/                      # Módulo de ontología RDF/OWL-RL
│   ├── difuso/                         # Módulo de lógica difusa (Scikit-Fuzzy)
│   ├── experto/                        # Módulo de sistema experto (Experta)
│   └── integrador/                     # Traductor dinámico Grafo -> Experta
├── tests/                              # Pruebas automatizadas (pytest)
├── sistema_hibrido.ipynb               # Notebook principal de orquestación y demo
├── pyproject.toml
└── README.md
```

---

## 👥 Repartición de Módulos y Roles

| Integrante | Módulo | Responsabilidad |
| :--- | :--- | :--- |
| **Integrante 1** | Lógica Difusa | Funciones de pertenencia, modificadores y defuzzificación (`src/difuso/`). |
| **Integrante 2** | Ontología | Construcción en Turtle, OWL-RL y casos de inferencia (`src/ontologia/`, `data/`). |
| **Integrante 3** | Sistema Experto | Hechos, reglas jurídicas, salience y control de bucles (`src/experto/`). |
| **Integrante 4** | Integrador | Traductor dinámico, demo orquestada y consolidación (`src/integrador/`). |

Consulta los detalles de los contratos de entrada y salida en [`docs/arquitectura_y_contratos.md`](docs/arquitectura_y_contratos.md).

---

## 🚀 Requisitos y Configuración

- **Python:** Python ≥ 3.10 (ver análisis de compatibilidad de `experta` en [`docs/compatibilidad_python_experta.md`](docs/compatibilidad_python_experta.md)).
- **Gestor de dependencias:** [uv](https://docs.astral.sh/uv/) o entorno virtual estándar `venv`.

```bash
# Instalación de librerías y sincronización del entorno
uv sync
```

---

## 🌿 Flujo de Trabajo en Git

1. Cada integrante trabaja sobre su rama personal: `feature/<nombre-integrante>`.
2. Realizar `push` a su propia rama remota.
3. Abrir Pull Request (PR) hacia `main` describiendo los cambios.
4. El propietario del repositorio revisa y realiza el merge a `main`.