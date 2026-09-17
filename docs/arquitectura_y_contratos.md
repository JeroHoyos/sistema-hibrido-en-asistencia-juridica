# Arquitectura del Sistema y Contratos de Interfaz

**Proyecto:** Sistema Híbrido en Asistencia Jurídica  
**Curso:** Introducción a la Inteligencia Artificial (UNAL Medellín)  
**Profesor:** Jaime Alberto Guzmán Luna  

---

## 1. Organización del Equipo y Roles

| Integrante | Módulo Asignado | Subdirectorio | Tecnologías Clave |
| :--- | :--- | :--- | :--- |
| **Integrante 1** | Lógica Difusa | `src/difuso/` | `scikit-fuzzy`, `numpy`, `matplotlib` |
| **Integrante 2** | Ontología y Razonamiento Semántico | `src/ontologia/` + `data/` | `rdflib`, `owlrl` (Turtle `.ttl`) |
| **Integrante 3** | Sistema Experto | `src/experto/` | `experta` (Hechos, Reglas, Salience) |
| **Integrante4 ** | Traductor Dinámico e Integración | `src/integrador/` | RDFLib $\rightarrow$ Experta, demo `.ipynb` |

---

## 2. Contratos de Interfaz (Flujo de Datos)

```
 [Ontología RDF/OWL-RL]
          │
          ▼ (Grafo semántico inferido)
 [Traductor Dinámico]  ──────────►  [Sistema Experto]  ◄─────────── [Lógica Difusa]
 (Consulta dinámicamente)         (Reglas de Inferencia)     (Urgencia / Viabilidad defuzzificada)
                                           │
                                           ▼
                                 [Dictamen Legal Final]
```

### Contrato 1: Ontología $\rightarrow$ Traductor
- **Origen:** Grafo generado tras aplicar `DeductiveClosure(RDFS_Semantics)` sobre `data/ontologia_juridica.ttl`.
- **Formato:** Objeto `rdflib.Graph`.
- **Regla Estricta:** El traductor debe leer dinámicamente los triples del grafo sin código duro ni nombres fijos.

### Contrato 2: Traductor $\rightarrow$ Sistema Experto
- **Salida:** Instancias de hechos que heredan de `experta.Fact` (ej. `CasoJuridico(...)`, `InvolucraPersona(...)`, `HechoDeducido(...)`).
- **Caso de prueba obligatorio:** Agregar un triple al `.ttl` sin tocar Python y verificar que se convierte a `Fact` en Experta.

### Contrato 3: Lógica Difusa $\rightarrow$ Sistema Experto
- **Entradas Difusas:** `Gravedad_Dano` (0-10), `Tiempo_Transcurrido_Meses` (0-36), `Vulnerabilidad_Economica` (0-100).
- **Salida Difusa:** `Nivel_Urgencia` continuo (0-100%) defuzzificado vía Centroide, más la etiqueta lingüística predominante (`BAJA`, `MEDIA`, `ALTA`).
- **Inyección en Experta:** Se declara un hecho `EvaluacionDifusa(urgencia_score=..., categoria='ALTA')` que actúa como precondición para activar reglas prioritarias (ej. medidas cautelares inmediatas).

---

## 3. Protocolo de Trabajo en Git

1. Cada integrante trabaja en su propia rama (`feature/<nombre>`).
2. Cada integrante programa dentro de su submódulo en `src/`.
3. Para integrar, hacer `push` a su rama y abrir Pull Request hacia `main`.
4. El propietario del repositorio revisa y realiza el merge a `main`.
5. El archivo `sistema_hibrido.ipynb` solo se edita para enlazar la demo final importando desde `src`.
