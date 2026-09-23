import collections.abc
import collections
if not hasattr(collections, 'Mapping'):
    collections.Mapping = collections.abc.Mapping

import os
from typing import Dict, Any, List, Optional
from rdflib import Graph, URIRef, Literal, RDF, RDFS
from experta import KnowledgeEngine

from src.experto.hechos import (
    Consulta,
    AutoridadCompetente,
    FuenteOficial,
    Recomendacion,
    HechoSemantico,
)
from src.ontologia.razonador import (
    cargar_ontologia,
    aplicar_razonador,
    EX,
)


# Extrae el identificador legible o fragmento final de una URI o Literal
def extraer_identificador_local(nodo: Any) -> str:
    # Remueve el prefijo de namespace para obtener el nombre conceptual limpio
    texto = str(nodo).strip()
    if "#" in texto:
        return texto.split("#")[-1]
    if ":" in texto and not texto.startswith("http"):
        return texto.split(":")[-1]
    if "/" in texto:
        return texto.split("/")[-1]
    return texto



# Determina si un triple corresponde al dominio modelado y no a axiomas internos
def es_triple_del_dominio(sujeto: Any, predicado: Any, objeto: Any, uri_base: str) -> bool:
    # Filtra relaciones internas del estandar W3C para enfocar la atencion en hechos del caso
    s_str, p_str, o_str = str(sujeto), str(predicado), str(objeto)
    return (
        uri_base in s_str or
        uri_base in p_str or
        uri_base in o_str or
        p_str.endswith("#type")
    )


# Convierte un triple semantico en hechos estructurados compatibles con experta
def mapear_triple_a_hechos(sujeto_id: str, predicado_id: str, objeto_id: str, objeto_raw: Any) -> List[Any]:
    # Produce hechos tipados segun el rol de la propiedad semantica
    hechos = []

    # Hecho semantico universal para trazabilidad completa de relaciones
    hechos.append(HechoSemantico(sujeto=sujeto_id, relacion=predicado_id, objeto=objeto_id))

    # Mapeo dinamico de propiedades funcionales a hechos operativos del sistema experto
    if predicado_id == "remitidoA":
        hechos.append(AutoridadCompetente(caso_id=sujeto_id, entidad=objeto_id))
    elif predicado_id == "fundamentadoEn":
        hechos.append(FuenteOficial(caso_id=sujeto_id, norma=objeto_id))
    elif predicado_id == "requiereMedida":
        hechos.append(Recomendacion(caso_id=sujeto_id, tipo_ayuda=objeto_id))
    elif predicado_id in ("type", "22-rdf-syntax-ns#type"):
        if objeto_id.startswith("Caso") and objeto_id != "CasoJuridico":
            hechos.append(Consulta(caso_id=sujeto_id, categoria=objeto_id.lower(), tipo=sujeto_id))
    elif predicado_id in ("descripcionHecho", "description"):
        hechos.append(Consulta(caso_id=sujeto_id, descripcion=str(objeto_raw)))

    return hechos


# Recorre el grafo deducido y pobla dinamicamente la memoria de trabajo del motor
def traducir_grafo_a_experta(grafo_inferido: Graph, motor: KnowledgeEngine, uri_base: Optional[str] = None) -> int:
    # Garantiza una integracion desacoplada sin depender de nombres fijos
    if uri_base is None:
        uri_base = str(EX)

    total_declarados = 0
    triples_procesados = set()

    for sujeto, predicado, objeto in grafo_inferido:
        if not es_triple_del_dominio(sujeto, predicado, objeto, uri_base):
            continue

        clave = (str(sujeto), str(predicado), str(objeto))
        if clave in triples_procesados:
            continue
        triples_procesados.add(clave)

        s_id = extraer_identificador_local(sujeto)
        p_id = extraer_identificador_local(predicado)
        o_id = extraer_identificador_local(objeto)

        hechos = mapear_triple_a_hechos(s_id, p_id, o_id, objeto)
        for h in hechos:
            motor.declare(h)
            total_declarados += 1

    return total_declarados


# Verifica el desacoplamiento modificando el archivo .ttl y comprobando la inferencia
def ejecutar_caso_prueba_obligatorio(ruta_ttl: str, nuevo_triple_ttl: str, motor: Optional[KnowledgeEngine] = None) -> bool:
    # Comprueba que cualquier nuevo triple en Turtle genera facts sin tocar codigo Python
    if not os.path.exists(ruta_ttl):
        raise FileNotFoundError(f"No se encontro el archivo de ontologia: {ruta_ttl}")

    with open(ruta_ttl, "r", encoding="utf-8") as f:
        contenido_original = f.read()

    try:
        # Se agrega el nuevo triple directamente al archivo .ttl
        with open(ruta_ttl, "a", encoding="utf-8") as f:
            f.write(f"\n{nuevo_triple_ttl}\n")

        # Se recarga la ontologia y se aplica el razonador RDFS
        grafo = cargar_ontologia(ruta_ttl)
        grafo_expandido = aplicar_razonador(grafo)

        # Se inicializa el motor si no fue provisto
        from src.experto.motor import AsistenteJuridico
        engine = motor if motor is not None else AsistenteJuridico()
        engine.reset()

        # Se realiza la traduccion dinamica a experta
        traducir_grafo_a_experta(grafo_expandido, engine)

        # Se extrae el sujeto del nuevo triple para validar su existencia en la memoria
        lineas = [l.strip() for l in nuevo_triple_ttl.strip().splitlines() if l.strip() and not l.strip().startswith("#")]
        if not lineas:
            return False

        sujeto_candidato = lineas[0].split()[0]
        sujeto_limpio = extraer_identificador_local(sujeto_candidato)

        # Verifica si existe al menos un hecho asociado al nuevo sujeto
        hecho_encontrado = any(
            (isinstance(f, HechoSemantico) and f.get("sujeto") == sujeto_limpio) or
            (isinstance(f, (Consulta, AutoridadCompetente, FuenteOficial, Recomendacion)) and f.get("caso_id") == sujeto_limpio)
            for f in engine.facts.values()
        )

        return hecho_encontrado

    finally:
        # Restaura fielmente el contenido del archivo para no alterar el repositorio
        with open(ruta_ttl, "w", encoding="utf-8") as f:
            f.write(contenido_original)


# Alias de compatibilidad funcional para invocaciones alternativas
probar_caso_obligatorio = ejecutar_caso_prueba_obligatorio
