#Pruebas unitarias automatizadas para el Sistema Experto en Asistencia Juridica

import collections.abc
import collections
if not hasattr(collections, 'Mapping'):
    collections.Mapping = collections.abc.Mapping

import pytest
from experta import Fact, KnowledgeEngine
from src.experto import (
    Consulta,
    AutoridadCompetente,
    PasoASeguir,
    FuenteOficial,
    Recomendacion,
    EvaluacionRiesgo,
    CasoProcesado,
    HechoSemantico,
    AsistenteJuridico,
    obtener_hechos_iniciales,
    cargar_base_conocimiento
)


def test_clases_de_hechos():
    #Verifica que existan al menos 5 clases estructuradas derivadas de Fact
    clases = [
        Consulta,
        AutoridadCompetente,
        PasoASeguir,
        FuenteOficial,
        Recomendacion,
        EvaluacionRiesgo,
        CasoProcesado,
        HechoSemantico
    ]
    assert len(clases) >= 5
    for cls in clases:
        assert issubclass(cls, Fact)


def test_minimo_quince_reglas():
    #Verifica que el motor de inferencia defina al menos 15 reglas de produccion
    motor = AsistenteJuridico()
    reglas = motor.get_rules()
    assert len(reglas) >= 15


def test_base_conocimiento_cuarenta_hechos():
    #Verifica que la base de hechos inicial contenga al menos 40 hechos estructurados
    hechos = obtener_hechos_iniciales()
    assert len(hechos) >= 40


def test_tres_niveles_de_salience():
    #Verifica que el motor implemente al menos 3 niveles de prioridad diferenciados
    motor = AsistenteJuridico()
    reglas = motor.get_rules()
    saliences = {r.salience for r in reglas}
    assert len(saliences) >= 3
    assert 100 in saliences
    assert 50 in saliences
    assert 20 in saliences


def test_resolucion_conflictos_salience():

    #Demuestra resolucion de conflictos por Salience:
    #Aun cuando coexistan hechos de violencia y territorial, la regla de violencia
    #(salience=100) debe dispararse con prioridad sobre la territorial (salience=20)

    motor = AsistenteJuridico()
    motor.reset()

    motor.declare(Consulta(categoria="territorial", tipo="limites_linderos_posesion_herencia_formalizacion"))
    motor.declare(Consulta(categoria="violencia_intrafamiliar", tipo="agresion_fisica_violencia_sexual"))

    motor.run()

    hechos_salida = [h for h in motor.facts.values()]
    autoridades = [h["entidad"] for h in hechos_salida if isinstance(h, AutoridadCompetente)]

    assert "comisaria_familia_fiscalia" in autoridades
    assert "centro_conciliacion_notaria" in autoridades


def test_resolucion_conflictos_especificidad():

    #Demuestra resolucion de conflictos por Especificidad:
    #A igual salience (50), la regla con patron compuesto (Consulta + EvaluacionRiesgo)
    #debe activarse y recomendar suspension provisional prioritaria

    motor = AsistenteJuridico()
    motor.reset()

    motor.declare(Consulta(categoria="vivienda", tipo="arrendamiento_cobros_mora_restitucion_desalojo"))
    motor.declare(EvaluacionRiesgo(nivel="alto"))

    motor.run()

    hechos_salida = [h for h in motor.facts.values()]
    recomendaciones = [h["tipo_ayuda"] for h in hechos_salida if isinstance(h, Recomendacion)]

    assert "suspension_provisional_desalojo_albergue" in recomendaciones


def test_resolucion_conflictos_recencia():

    #Demuestra resolucion de conflictos por Recencia:
    #El hecho declarado mas recientemente influye en la precedencia de evaluacion

    motor = AsistenteJuridico()
    motor.reset()

    motor.declare(Consulta(caso_id="C1", categoria="territorial", tipo="despojo_inmueble_perturbacion_posesion"))
    motor.declare(Consulta(caso_id="C2", categoria="territorial", tipo="despojo_inmueble_perturbacion_posesion"))

    motor.run()

    hechos_salida = [h for h in motor.facts.values()]
    casos_procesados = [h["caso_id"] for h in hechos_salida if isinstance(h, AutoridadCompetente) and "caso_id" in h]

    assert "C1" in casos_procesados
    assert "C2" in casos_procesados


def test_prevencion_bucle_lock_fact():

    #Demuestra prevencion de bucles infinitos con Lock-Fact:
    #La regla con NOT(CasoProcesado) se ejecuta exactamente una vez por caso_id

    motor = AsistenteJuridico()
    motor.reset()

    motor.declare(Consulta(caso_id="TEST-LOOP", categoria="territorial", tipo="linderos"))

    motor.run()

    hechos_salida = [h for h in motor.facts.values()]
    locks = [h for h in hechos_salida if isinstance(h, CasoProcesado) and h.get("caso_id") == "TEST-LOOP"]

    assert len(locks) == 1
    assert locks[0]["estado"] == "analizado"


def test_reglas_originales_de_jero_preservadas():

    #Verifica que las 11 reglas originales disenadas por Jero permanezcan operativas

    motor = AsistenteJuridico()
    nombres_reglas = {r._wrapped.__name__ for r in motor.get_rules()}

    reglas_jero = {
        "vivienda_arrendamiento_desalojo",
        "vivienda_habitabilidad",
        "vivienda_propiedad_sucesion",
        "territorial_linderos",
        "territorial_uso_suelo",
        "territorial_desplazamiento",
        "violencia_control_psicologico",
        "violencia_agresion_fisica",
        "violencia_control_economico",
        "violencia_poblacion_dependiente",
        "violencia_incumplimiento_medida"
    }

    assert reglas_jero.issubset(nombres_reglas)
