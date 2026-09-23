import collections.abc
import collections
if not hasattr(collections, 'Mapping'):
    collections.Mapping = collections.abc.Mapping

import pytest
from rdflib import Graph, Namespace, URIRef, Literal, RDF
from src.experto.motor import AsistenteJuridico
from src.experto.hechos import (
    Consulta,
    AutoridadCompetente,
    FuenteOficial,
    Recomendacion,
    HechoSemantico
)
from src.ontologia.razonador import (
    cargar_ontologia,
    aplicar_razonador,
    EX
)
from src.integrador.traductor import (
    traducir_grafo_a_experta,
    ejecutar_caso_prueba_obligatorio,
    probar_caso_obligatorio,
    extraer_identificador_local,
    mapear_triple_a_hechos
)

RUTA_TTL = "data/ontologia_juridica.ttl"


def test_traduccion_dinamica_grafo_a_experta():
    # Comprueba la conversion automatica de triples RDF a hechos de experta sin cableado
    grafo = cargar_ontologia(RUTA_TTL)
    grafo_inferido = aplicar_razonador(grafo)

    motor = AsistenteJuridico()
    motor.reset()

    total_declarados = traducir_grafo_a_experta(grafo_inferido, motor)
    assert total_declarados > 0
    assert len(motor.facts) > 100

    # Comprueba la presencia de hechos semanticos genericos y hechos estructurados
    hechos_semanticos = [f for f in motor.facts.values() if isinstance(f, HechoSemantico)]
    autoridades = [f for f in motor.facts.values() if isinstance(f, AutoridadCompetente)]
    fuentes = [f for f in motor.facts.values() if isinstance(f, FuenteOficial)]
    recomendaciones = [f for f in motor.facts.values() if isinstance(f, Recomendacion)]

    assert len(hechos_semanticos) > 0
    assert len(autoridades) > 0
    assert len(fuentes) > 0
    assert len(recomendaciones) > 0


def test_traduccion_sin_cablear_valores_arbitrarios():
    # Valida la generalidad del algoritmo sobre identificadores y relaciones arbitrarias
    grafo_sintetico = Graph()
    grafo_sintetico.bind("ex", EX)
    
    sujeto_arbitrario = EX.caso_desconocido_999
    grafo_sintetico.add((sujeto_arbitrario, EX.remitidoA, EX.entidad_sintetica_888))
    grafo_sintetico.add((sujeto_arbitrario, EX.fundamentadoEn, EX.norma_arbitraria_777))
    grafo_sintetico.add((sujeto_arbitrario, EX.requiereMedida, EX.medida_cautelar_666))

    motor = AsistenteJuridico()
    motor.reset()

    traducir_grafo_a_experta(grafo_sintetico, motor)

    # Verifica la creacion dinamica sin importar la novedad de los identificadores
    claves_sujeto = {f.get("caso_id") for f in motor.facts.values() if "caso_id" in f}
    assert "caso_desconocido_999" in claves_sujeto

    entidades = {f.get("entidad") for f in motor.facts.values() if isinstance(f, AutoridadCompetente)}
    assert "entidad_sintetica_888" in entidades


def test_caso_prueba_obligatorio_integracion_ttl():
    # Comprueba la prueba obligatoria agregando un nuevo individuo directo al Turtle
    nuevo_triple = (
        "ex:caso_automatizado_test a ex:CasoViolencia ;\n"
        "    ex:remitidoA ex:comisaria_familia ;\n"
        "    ex:fundamentadoEn ex:ley_1257_2008 ."
    )

    with open(RUTA_TTL, "r", encoding="utf-8") as f:
        contenido_previo = f.read()

    resultado = ejecutar_caso_prueba_obligatorio(RUTA_TTL, nuevo_triple)
    assert resultado is True

    # Verifica que el archivo Turtle haya sido restaurado a su estado original
    with open(RUTA_TTL, "r", encoding="utf-8") as f:
        contenido_posterior = f.read()

    assert contenido_previo == contenido_posterior
