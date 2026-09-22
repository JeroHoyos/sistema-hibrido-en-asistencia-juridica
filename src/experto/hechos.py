#Definicion de clases Fact para estructurar la memoria de trabajo del sistema experto

import collections.abc
import collections
if not hasattr(collections, 'Mapping'):
    collections.Mapping = collections.abc.Mapping

from experta import Fact


class Consulta(Fact):
    """
    Representa el caso consultado por el ciudadano
    Campos tipicos: caso_id, categoria, tipo, descripcion
    """
    pass


class AutoridadCompetente(Fact):
    """
    Identifica la entidad juridica o administrativa a la que se remite el caso
    Campos tipicos: caso_id, entidad, sede
    """
    pass


class PasoASeguir(Fact):
    """
    Define un tramite o etapa procesal ordenada que debe surtirse
    Campos tipicos: caso_id, orden, accion
    """
    pass


class FuenteOficial(Fact):
    """
    Identifica la norma legal que fundamenta la orientacion juridica
    Campos tipicos: caso_id, norma, articulo
    """
    pass


class Recomendacion(Fact):
    """
    Dictamen final emitido por el sistema experto hacia el ciudadano
    Campos tipicos: caso_id, tipo_ayuda, prioridad
    """
    pass


class EvaluacionRiesgo(Fact):
    """
    Integra la salida numerica y linguistica del motor de logica difusa
    Campos tipicos: caso_id, urgencia_score, nivel
    """
    pass


class CasoProcesado(Fact):
    """
    Hecho de bloqueo (Lock-Fact) para prevenir la reactivacion y bucles infinitos
    Campos tipicos: caso_id, regla
    """
    pass


class HechoSemantico(Fact):
    """
    Encapsula triples inferidos dinamicamente desde la ontologia RDF/OWL-RL
    Campos tipicos: sujeto, relacion, objeto
    """
    pass
