#Motor de inferencia del Sistema Experto en Asistencia Juridica

import collections.abc
import collections
if not hasattr(collections, 'Mapping'):
    collections.Mapping = collections.abc.Mapping

from experta import KnowledgeEngine, Rule, Fact, MATCH, AS, NOT
from src.experto.hechos import (
    Consulta,
    AutoridadCompetente,
    PasoASeguir,
    FuenteOficial,
    Recomendacion,
    EvaluacionRiesgo,
    CasoProcesado,
    HechoSemantico
)


class AsistenteJuridico(KnowledgeEngine):

    #Motor de reglas para clasificar consultas juridicas y asignar rutas procesales
    #Controla el orden de inferencia mediante salience, resuelve conflictos por
    #especificidad y recencia, y previene recursiones infinitas mediante Lock-Fact



    # Nivel 1: Violencia Intrafamiliar (Salience = 100)
    # Justificacion: Amenaza inminente a la vida, integridad personal o menores.


    @Rule(
        Consulta(categoria="violencia_intrafamiliar", tipo="insultos_amenazas_control_aislamiento_vigilancia"),
        salience=100
    )
    def violencia_control_psicologico(self):
        #Atiende violencia verbal y psicologica para mitigar escalamiento delictivo
        self.declare(AutoridadCompetente(entidad="comisaria_familia"))
        self.declare(FuenteOficial(norma="Ley_1257_de_2008"))
        self.declare(Recomendacion(tipo_ayuda="apoyo_psicosocial"))
        self.declare(PasoASeguir(accion="solicitar_audiencia_conciliacion_y_medida_alejamiento"))

    @Rule(
        Consulta(categoria="violencia_intrafamiliar", tipo="agresion_fisica_violencia_sexual"),
        salience=100
    )
    def violencia_agresion_fisica(self):
        #Activa la ruta penal y de medidas cautelares por delitos contra la integridad fisica
        self.declare(AutoridadCompetente(entidad="comisaria_familia_fiscalia"))
        self.declare(FuenteOficial(norma="Ley_1257_de_2008"))
        self.declare(Recomendacion(tipo_ayuda="medida_proteccion_urgente"))
        self.declare(PasoASeguir(accion="remision_medicina_legal_y_desalojo_agresor"))

    @Rule(
        Consulta(categoria="violencia_intrafamiliar", tipo="control_dinero_apropiacion_bienes"),
        salience=100
    )
    def violencia_control_economico(self):
        #Protege la subsistencia y el patrimonio retenido indebidamente dentro del nucleo familiar
        self.declare(AutoridadCompetente(entidad="comisaria_familia"))
        self.declare(FuenteOficial(norma="Ley_1257_de_2008_art_2"))
        self.declare(Recomendacion(tipo_ayuda="orientacion_juridica_patrimonial"))
        self.declare(PasoASeguir(accion="inventario_de_bienes_y_fijacion_alimentos"))

    @Rule(
        Consulta(categoria="violencia_intrafamiliar", tipo="violencia_negligencia_ninos_mayores_discapacidad"),
        salience=100
    )
    def violencia_poblacion_dependiente(self):
        #Prioriza a sujetos de especial proteccion constitucional mediante intervencion del ICBF
        self.declare(AutoridadCompetente(entidad="icbf_comisaria_familia"))
        self.declare(FuenteOficial(norma="Codigo_Infancia_Adolescencia_Ley_1098"))
        self.declare(Recomendacion(tipo_ayuda="proteccion_poblacion_dependiente"))
        self.declare(PasoASeguir(accion="verificacion_garantia_derechos_y_custodia"))

    @Rule(
        Consulta(categoria="violencia_intrafamiliar", tipo="incumplimiento_medida_atencion_inadecuada"),
        salience=100
    )
    def violencia_incumplimiento_medida(self):
        #Inicia tramite incidental de desacato y remision por fraude a resolucion judicial
        self.declare(AutoridadCompetente(entidad="comisaria_familia"))
        self.declare(FuenteOficial(norma="Ley_294_de_1996_art_7"))
        self.declare(Recomendacion(tipo_ayuda="reactivar_ruta_proteccion"))
        self.declare(PasoASeguir(accion="apertura_incidente_desacato_y_arresto"))

    @Rule(
        Consulta(categoria="violencia_intrafamiliar", tipo="amenaza_muerte_armas_riesgo_extremo"),
        EvaluacionRiesgo(nivel="critico"),
        salience=100
    )
    def violencia_riesgo_extremo_medida_cautelar(self):
        #Coordina proteccion policial inmediata por amenaza inminente con armas calificada por logica difusa
        self.declare(AutoridadCompetente(entidad="policia_nacional_fiscalia_cTI"))
        self.declare(FuenteOficial(norma="Constitucion_Politica_art_11"))
        self.declare(Recomendacion(tipo_ayuda="traslado_casa_refugio_y_seguridad_policial"))
        self.declare(PasoASeguir(accion="orden_captura_en_flagrancia_y_esquema_proteccion"))


    # Nivel 2: Vivienda (Salience = 50)
    # Justificacion: Afectacion a derechos patrimoniales y condiciones de habitabilidad.


    @Rule(
        Consulta(categoria="vivienda", tipo="arrendamiento_cobros_mora_restitucion_desalojo"),
        salience=50
    )
    def vivienda_arrendamiento_desalojo(self):
        #Encauza controversias contractuales de arrendamiento ante la jurisdiccion civil ordinaria.
        self.declare(AutoridadCompetente(entidad="juzgado_civil"))
        self.declare(FuenteOficial(norma="Ley_820_de_2003"))
        self.declare(Recomendacion(tipo_ayuda="asesoria_restitucion"))
        self.declare(PasoASeguir(accion="notificacion_requerimiento_pago_y_demanda"))

    @Rule(
        Consulta(categoria="vivienda", tipo="arrendamiento_cobros_mora_restitucion_desalojo"),
        EvaluacionRiesgo(nivel="alto"),
        salience=50
    )
    def vivienda_desalojo_vulnerabilidad_alta(self):
        #Demuestra resolucion de conflictos por Especificidad
        #Al coincidir con la regla general de salience=50, el motor prioriza esta regla
        #compuesta por exigir un patron adicional de riesgo elevado.

        self.declare(AutoridadCompetente(entidad="personeria_juzgado_civil"))
        self.declare(FuenteOficial(norma="Sentencia_T_058_Corte_Constitucional"))
        self.declare(Recomendacion(tipo_ayuda="suspension_provisional_desalojo_albergue"))
        self.declare(PasoASeguir(accion="interponer_tutela_por_sujeto_especial_proteccion"))

    @Rule(
        Consulta(categoria="vivienda", tipo="habitabilidad_servicios_publicos_construccion"),
        salience=50
    )
    def vivienda_habitabilidad(self):
        #Tutela el acceso minimo a servicios publicos como parte de la dignidad humana
        self.declare(AutoridadCompetente(entidad="personeria"))
        self.declare(FuenteOficial(norma="Ley_142_de_1994"))
        self.declare(Recomendacion(tipo_ayuda="reporte_habitabilidad"))
        self.declare(PasoASeguir(accion="interposicion_reclamo_empresa_servicios_y_tutela"))

    @Rule(
        Consulta(categoria="vivienda", tipo="propiedad_escritura_sucesion_subsidios_reubicacion"),
        salience=50
    )
    def vivienda_propiedad_sucesion(self):
        #Orienta tramites notariales y judiciales para formalizar la propiedad inmobiliaria
        self.declare(AutoridadCompetente(entidad="consultorio_juridico_notaria"))
        self.declare(FuenteOficial(norma="Codigo_Civil_sucesiones"))
        self.declare(Recomendacion(tipo_ayuda="consultorio_juridico_titulacion"))
        self.declare(PasoASeguir(accion="estudio_titulos_y_sucesion_notarial"))

    @Rule(
        Consulta(categoria="vivienda", tipo="defectos_construccion_amenaza_ruina"),
        salience=50
    )
    def vivienda_riesgo_ruina(self):
        #Acciona el amparo policivo para prevenir siniestros por fallas estructurales
        self.declare(AutoridadCompetente(entidad="inspeccion_policia_dagrd"))
        self.declare(FuenteOficial(norma="Codigo_Civil_art_988_ruina"))
        self.declare(Recomendacion(tipo_ayuda="inspeccion_tecnica_urgente_y_desalojo_preventivo"))
        self.declare(PasoASeguir(accion="solicitud_visita_gestion_riesgo_y_querella"))


    # Nivel 3: Conflictos Territoriales (Salience = 20)
    # Justificacion: Conflictos sobre limites, licencias y tramite administrativo.


    @Rule(
        Consulta(categoria="territorial", tipo="limites_linderos_posesion_herencia_formalizacion"),
        salience=20
    )
    def territorial_linderos(self):
        #Promueve la resolucion alternativa de conflictos antes de acudir a litigio declarativo
        self.declare(AutoridadCompetente(entidad="centro_conciliacion_notaria"))
        self.declare(FuenteOficial(norma="Codigo_General_Proceso_art_372"))
        self.declare(Recomendacion(tipo_ayuda="centro_conciliacion"))
        self.declare(PasoASeguir(accion="solicitud_audiencia_fijacion_linderos"))

    @Rule(
        Consulta(categoria="territorial", tipo="uso_suelo_licencias_espacio_publico_informalidad"),
        salience=20
    )
    def territorial_uso_suelo(self):
        #Verifica la conformidad urbanistica del predio segun el Plan de Ordenamiento Territorial
        self.declare(AutoridadCompetente(entidad="curaduria_urbana_planeacion"))
        self.declare(FuenteOficial(norma="Ley_388_de_1997_POT"))
        self.declare(Recomendacion(tipo_ayuda="consulta_plan_ordenamiento"))
        self.declare(PasoASeguir(accion="solicitar_concepto_uso_suelo_y_licencia"))

    @Rule(
        Consulta(categoria="territorial", tipo="desplazamiento_riesgo_desastre_afectacion_ambiental"),
        salience=20
    )
    def territorial_desplazamiento(self):
        #Activa el protocolo de inclusion en el Registro Unico de Victimas por despojo o desastre
        self.declare(AutoridadCompetente(entidad="unidad_victimas"))
        self.declare(FuenteOficial(norma="Ley_1448_de_2011"))
        self.declare(Recomendacion(tipo_ayuda="ruta_atencion_desplazamiento"))
        self.declare(PasoASeguir(accion="declaracion_ante_ministerio_publico"))

    @Rule(
        Consulta(categoria="territorial", tipo="afectacion_ambiental_recursos_colectivos"),
        salience=20
    )
    def territorial_afectacion_ambiental(self):
        #Canaliza denuncias sobre danos a fuentes hidricas y areas de reserva protegidas
        self.declare(AutoridadCompetente(entidad="corporacion_autonoma_regional_car"))
        self.declare(FuenteOficial(norma="Ley_99_de_1993"))
        self.declare(Recomendacion(tipo_ayuda="interposicion_accion_popular"))
        self.declare(PasoASeguir(accion="denuncia_ambiental_y_medida_cautelar_cese"))

    @Rule(
        Consulta(caso_id=MATCH.cid, categoria="territorial", tipo="despojo_inmueble_perturbacion_posesion"),
        salience=20
    )
    def territorial_despojo_reciente(self, cid):

        #Demuestra resolucion de conflictos por Recencia
        #Cuando coinciden casos del mismo nivel, el motor prioriza el hecho ingresado
        #mas recientemente en la memoria de trabajo

        self.declare(AutoridadCompetente(caso_id=cid, entidad="inspeccion_policia"))
        self.declare(FuenteOficial(caso_id=cid, norma="Codigo_Nacional_Policia_Ley_1801"))
        self.declare(Recomendacion(caso_id=cid, tipo_ayuda="accion_policiva_amparo_posesorio"))
        self.declare(PasoASeguir(caso_id=cid, accion="interposicion_querella_antes_de_4_meses"))


    # Control de Bucles Infinitos: Mecanismo Lock-Fact
    # Justificacion: Garantiza terminacion del algoritmo al iterar hechos derivados.


    @Rule(
        AS.caso << Consulta(caso_id=MATCH.cid),
        NOT(CasoProcesado(caso_id=MATCH.cid)),
        salience=15
    )
    def control_prevencion_bucle_lock_fact(self, caso, cid):

        #Implementa el patron Lock-Fact. Al verificar que no existe CasoProcesado,
        #declara dicho hecho de bloqueo impidiendo que la agenda vuelva a evaluar
        #esta regla para el mismo caso en ciclos posteriores

        self.declare(CasoProcesado(caso_id=cid, estado="analizado"))


    # Cierre Administrativo (Salience = 10)
    # Justificacion: Ejecucion residual una vez agotadas las deducciones sustantivas.


    @Rule(
        CasoProcesado(caso_id=MATCH.cid, estado="analizado"),
        salience=10
    )
    def notificacion_cierre_tramite(self, cid):
        #Registra la finalizacion del analisis y consolida el expediente digital
        self.declare(PasoASeguir(caso_id=cid, accion="generacion_expediente_y_notificacion"))
