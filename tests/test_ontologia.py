# Pruebas automatizadas para el modelo ontologico y el razonador semantico

import pytest
from rdflib import RDF, RDFS, URIRef
from src.ontologia import (
    cargar_ontologia,
    aplicar_razonador,
    aplicar_razonamiento_rdfs,
    verificar_tres_casos_inferencia,
    verificar_casos_inferencia,
    obtener_nuevos_hechos,
    comparar_grafo_antes_despues,
    EX
)

RUTA_TTL = "data/ontologia_juridica.ttl"


@pytest.fixture(scope="module")
def grafo_base():
    # Carga la ontologia base serializada en Turtle
    return cargar_ontologia(RUTA_TTL)


@pytest.fixture(scope="module")
def grafo_inferido(grafo_base):
    # Ejecuta el motor semantico RDFS de owlrl
    return aplicar_razonador(grafo_base)


def test_clases_y_jerarquias_ontologia(grafo_base):
    # Comprueba la existencia de al menos 10 clases formales y 5 jerarquias subClassOf
    clases = set(grafo_base.subjects(RDF.type, RDFS.Class))
    subclases = list(grafo_base.subject_objects(RDFS.subClassOf))

    assert len(clases) >= 10
    assert len(subclases) >= 5
    assert (EX.CasoViolencia, RDFS.subClassOf, EX.CasoJuridico) in grafo_base
    assert (EX.CasoVivienda, RDFS.subClassOf, EX.CasoJuridico) in grafo_base
    assert (EX.CasoTerritorial, RDFS.subClassOf, EX.CasoJuridico) in grafo_base


def test_propiedades_dominio_y_rango(grafo_base):
    # Comprueba la definicion de al menos 10 propiedades con dominio, rango y jerarquia
    propiedades = set(grafo_base.subjects(RDF.type, RDF.Property))
    subpropiedades = list(grafo_base.subject_objects(RDFS.subPropertyOf))

    assert len(propiedades) >= 10
    assert len(subpropiedades) >= 1

    props_completas = [
        p for p in propiedades
        if (p, RDFS.domain, None) in grafo_base and (p, RDFS.range, None) in grafo_base
    ]
    assert len(props_completas) >= 10
    assert (EX.tieneVictima, RDFS.subPropertyOf, EX.involucraPersona) in grafo_base


def test_individuos_con_etiqueta_rdfs_label(grafo_base):
    # Comprueba la presencia de al menos 40 individuos documentados con rdfs:label
    individuos_con_label = set(grafo_base.subjects(RDFS.label, None))
    assert len(individuos_con_label) >= 40


def test_owlrl_tres_casos_inferencia_obligatorios(grafo_inferido):
    # Valida formalmente los 3 casos de deduccion deductiva exigidos por la guia docente
    resultados = verificar_tres_casos_inferencia(grafo_inferido)

    # Caso 1: Individuo infiere clase padre por herencia subClassOf
    assert resultados["caso_1_subclass"] is True
    assert (EX.caso_violencia_01, RDF.type, EX.CasoJuridico) in grafo_inferido

    # Caso 2: Inferencia de clases por axiomas de dominio y rango en propiedad
    assert resultados["caso_2_domain_range"] is True
    assert (EX.caso_prueba_inferencia, RDF.type, EX.CasoJuridico) in grafo_inferido
    assert (EX.sujeto_inferido_victima, RDF.type, EX.Victima) in grafo_inferido

    # Caso 3: Inferencia de relacion padre por jerarquia subPropertyOf
    assert resultados["caso_3_subproperty"] is True
    assert (EX.caso_violencia_01, EX.involucraPersona, EX.victima_01) in grafo_inferido


def test_owlrl_minimo_cuatro_nuevos_hechos(grafo_base, grafo_inferido):
    # Comprueba que el razonador derive al menos 4 nuevos triples ausentes en el grafo inicial
    nuevos = obtener_nuevos_hechos(grafo_base, grafo_inferido)
    total_nuevos, lista_nuevos = comparar_grafo_antes_despues(grafo_base, grafo_inferido)

    assert len(nuevos) >= 4
    assert total_nuevos == len(nuevos)
    assert len(grafo_inferido) > len(grafo_base)
