# Modulo integrador entre la ontologia semantica y el sistema experto

from src.integrador.traductor import (
    traducir_grafo_a_experta,
    ejecutar_caso_prueba_obligatorio,
    probar_caso_obligatorio,
    extraer_identificador_local,
    mapear_triple_a_hechos
)

__all__ = [
    "traducir_grafo_a_experta",
    "ejecutar_caso_prueba_obligatorio",
    "probar_caso_obligatorio",
    "extraer_identificador_local",
    "mapear_triple_a_hechos"
]
