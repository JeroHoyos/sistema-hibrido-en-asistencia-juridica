#Base de conocimiento inicial para el sistema experto

from src.experto.hechos import (
    Consulta,
    AutoridadCompetente,
    PasoASeguir,
    FuenteOficial,
    EvaluacionRiesgo,
    HechoSemantico
)


def obtener_hechos_iniciales():

    # Retorna la lista de hechos iniciales del dominio juridico

    hechos = [
        #1. Marco Normativo Oficial (10 Hechos)
        FuenteOficial(norma_id="NORM-01", norma="Ley_1257_de_2008", materia="proteccion_violencia_genero"),
        FuenteOficial(norma_id="NORM-02", norma="Ley_820_de_2003", materia="arrendamiento_vivienda_urbana"),
        FuenteOficial(norma_id="NORM-03", norma="Ley_1448_de_2011", materia="atencion_reparacion_victimas"),
        FuenteOficial(norma_id="NORM-04", norma="Ley_1098_de_2006", materia="codigo_infancia_adolescencia"),
        FuenteOficial(norma_id="NORM-05", norma="Ley_388_de_1997", materia="desarrollo_territorial_y_pot"),
        FuenteOficial(norma_id="NORM-06", norma="Ley_294_de_1996", materia="violencia_intrafamiliar"),
        FuenteOficial(norma_id="NORM-07", norma="Ley_1801_de_2016", materia="codigo_nacional_de_policia"),
        FuenteOficial(norma_id="NORM-08", norma="Ley_142_de_1994", materia="servicios_publicos_domiciliarios"),
        FuenteOficial(norma_id="NORM-09", norma="Codigo_Civil_Libro_3", materia="sucesiones_y_donaciones"),
        FuenteOficial(norma_id="NORM-10", norma="Ley_99_de_1993", materia="medio_ambiente_y_recursos_naturales"),

        # 2. Autoridades e Instituciones Competentes (10 Hechos)
        AutoridadCompetente(entidad_id="AUT-01", entidad="comisaria_familia", tipo="administrativa_policiva"),
        AutoridadCompetente(entidad_id="AUT-02", entidad="fiscalia_general_nacion", tipo="judicial_penal"),
        AutoridadCompetente(entidad_id="AUT-03", entidad="juzgado_civil_municipal", tipo="judicial_civil"),
        AutoridadCompetente(entidad_id="AUT-04", entidad="personeria_municipal", tipo="ministerio_publico"),
        AutoridadCompetente(entidad_id="AUT-05", entidad="curaduria_urbana", tipo="urbanistica"),
        AutoridadCompetente(entidad_id="AUT-06", entidad="icbf_defensoria_familia", tipo="proteccion_menores"),
        AutoridadCompetente(entidad_id="AUT-07", entidad="unidad_para_las_victimas", tipo="atencion_desplazamiento"),
        AutoridadCompetente(entidad_id="AUT-08", entidad="centro_conciliacion_derecho", tipo="resolucion_alternativa"),
        AutoridadCompetente(entidad_id="AUT-09", entidad="inspeccion_policia", tipo="policiva_local"),
        AutoridadCompetente(entidad_id="AUT-10", entidad="corporacion_autonoma_regional", tipo="ambiental"),

        # 3. Pasos y Rutas Procesales (10 Hechos)
        PasoASeguir(paso_id="PASO-01", orden=1, accion="radicacion_solicitud_medida_proteccion"),
        PasoASeguir(paso_id="PASO-02", orden=2, accion="remision_medicina_legal_valoracion"),
        PasoASeguir(paso_id="PASO-03", orden=3, accion="citacion_audiencia_tramite_medida"),
        PasoASeguir(paso_id="PASO-04", orden=4, accion="orden_desalojo_inmediato_agresor"),
        PasoASeguir(paso_id="PASO-05", orden=1, accion="requerimiento_pago_por_mora"),
        PasoASeguir(paso_id="PASO-06", orden=2, accion="audiencia_conciliacion_restitucion"),
        PasoASeguir(paso_id="PASO-07", orden=3, accion="demanda_restitucion_inmueble_arrendado"),
        PasoASeguir(paso_id="PASO-08", orden=1, accion="declaracion_registro_unico_victimas"),
        PasoASeguir(paso_id="PASO-09", orden=2, accion="solicitud_ayuda_humanitaria_inmediata"),
        PasoASeguir(paso_id="PASO-10", orden=1, accion="interposicion_accion_popular_ambiental"),

        # 4. Casos Juridicos Registrados para Diagnostico (8 Hechos)
        Consulta(caso_id="CASO-01", categoria="violencia_intrafamiliar", tipo="agresion_fisica_violencia_sexual"),
        Consulta(caso_id="CASO-02", categoria="violencia_intrafamiliar", tipo="violencia_negligencia_ninos_mayores_discapacidad"),
        Consulta(caso_id="CASO-03", categoria="violencia_intrafamiliar", tipo="insultos_amenazas_control_aislamiento_vigilancia"),
        Consulta(caso_id="CASO-04", categoria="vivienda", tipo="arrendamiento_cobros_mora_restitucion_desalojo"),
        Consulta(caso_id="CASO-05", categoria="vivienda", tipo="habitabilidad_servicios_publicos_construccion"),
        Consulta(caso_id="CASO-06", categoria="vivienda", tipo="propiedad_escritura_sucesion_subsidios_reubicacion"),
        Consulta(caso_id="CASO-07", categoria="territorial", tipo="limites_linderos_posesion_herencia_formalizacion"),
        Consulta(caso_id="CASO-08", categoria="territorial", tipo="desplazamiento_riesgo_desastre_afectacion_ambiental"),

        # 5. Hechos de Integracion Difusa y Semantica (4 Hechos)
        EvaluacionRiesgo(caso_id="CASO-01", urgencia_score=92.5, nivel="critico"),
        EvaluacionRiesgo(caso_id="CASO-04", urgencia_score=78.0, nivel="alto"),
        HechoSemantico(sujeto="CASO-01", relacion="aplicaNorma", objeto="Ley_1257_de_2008"),
        HechoSemantico(sujeto="CASO-04", relacion="remitidoA", objeto="juzgado_civil")
    ]
    return hechos


def cargar_base_conocimiento(motor):

    #Declara los hechos iniciales dentro de la memoria de trabajo del motor

    hechos = obtener_hechos_iniciales()
    for h in hechos:
        motor.declare(h)
    return len(hechos)
