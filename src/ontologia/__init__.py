# Modulo de Ontologias y Razonamiento Semantico

from src.ontologia.razonador import (
    cargar_ontologia,
    aplicar_razonador,
    aplicar_razonamiento_rdfs,
    verificar_tres_casos_inferencia,
    verificar_casos_inferencia,
    obtener_nuevos_hechos,
    comparar_grafo_antes_despues,
    crear_grafo_con_namespaces,
    EX,
    DC
)

__all__ = [
    "cargar_ontologia",
    "aplicar_razonador",
    "aplicar_razonamiento_rdfs",
    "verificar_tres_casos_inferencia",
    "verificar_casos_inferencia",
    "obtener_nuevos_hechos",
    "comparar_grafo_antes_despues",
    "crear_grafo_con_namespaces",
    "EX",
    "DC"
]
