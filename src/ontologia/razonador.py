from rdflib import Graph, Namespace, URIRef, RDF, RDFS
from rdflib.namespace import FOAF, XSD
from owlrl import DeductiveClosure, RDFS_Semantics

# Definicion manual de namespaces y prefijos
EX = Namespace("http://example.org/juridico#")
DC = Namespace("http://purl.org/dc/elements/1.1/")


# Inicializa y vincula los prefijos uno a uno para garantizar serializacion estandar
def crear_grafo_con_namespaces():
    g = Graph()
    g.bind("ex", EX)
    g.bind("rdf", RDF)
    g.bind("rdfs", RDFS)
    g.bind("xsd", XSD)
    g.bind("foaf", FOAF)
    g.bind("dc", DC)
    return g


# Carga la ontologia desde el archivo Turtle serializado
def cargar_ontologia(ruta_ttl):
    g = crear_grafo_con_namespaces()
    g.parse(ruta_ttl, format="turtle")
    return g


# Ejecuta el motor semantico RDFS de owlrl para deducir afirmaciones implicitas
def aplicar_razonador(grafo):
    # Se crea una copia para poder comparar el estado previo contra el expandido
    grafo_expandido = Graph()
    for triple in grafo:
        grafo_expandido.add(triple)

    # Vinculacion de namespaces en el grafo expandido
    grafo_expandido.bind("ex", EX)
    grafo_expandido.bind("rdf", RDF)
    grafo_expandido.bind("rdfs", RDFS)
    grafo_expandido.bind("xsd", XSD)
    grafo_expandido.bind("foaf", FOAF)
    grafo_expandido.bind("dc", DC)

    # Inferencia formal aplicando la semantica de RDFS de W3C
    DeductiveClosure(RDFS_Semantics, axiomatic_triples=True, datatype_axioms=False).expand(grafo_expandido)
    return grafo_expandido


# Comprueba los tres casos de inferencia obligatorios
def verificar_tres_casos_inferencia(grafo_inferido):
    resultados = {
        "caso_1_subclass": False,
        "caso_2_domain_range": False,
        "caso_3_subproperty": False
    }

    # Caso 1: Individuo declarado como CasoViolencia infiere ser CasoJuridico por herencia
    caso_1 = (EX.caso_violencia_01, RDF.type, EX.CasoJuridico)
    if caso_1 in grafo_inferido:
        resultados["caso_1_subclass"] = True

    # Caso 2: Individuo infiere ser CasoJuridico por dominio y Victima por rango de tieneVictima
    caso_2_dom = (EX.caso_prueba_inferencia, RDF.type, EX.CasoJuridico)
    caso_2_ran = (EX.sujeto_inferido_victima, RDF.type, EX.Victima)
    if caso_2_dom in grafo_inferido and caso_2_ran in grafo_inferido:
        resultados["caso_2_domain_range"] = True

    # Caso 3: Triple con tieneVictima infiere la propiedad padre involucraPersona
    caso_3 = (EX.caso_violencia_01, EX.involucraPersona, EX.victima_01)
    if caso_3 in grafo_inferido:
        resultados["caso_3_subproperty"] = True

    return resultados


# Cuantifica y extrae los nuevos triples deducidos que no existian en el grafo original
def obtener_nuevos_hechos(grafo_base, grafo_inferido):
    triples_base = set(grafo_base)
    triples_inferidos = set(grafo_inferido)
    nuevos_hechos = triples_inferidos - triples_base
    return list(nuevos_hechos)


# Retorna el conteo y la coleccion de nuevos hechos inferidos
def comparar_grafo_antes_despues(grafo_base, grafo_inferido):
    nuevos = obtener_nuevos_hechos(grafo_base, grafo_inferido)
    return len(nuevos), nuevos


# Aliases para compatibilidad con diferentes nomenclaturas de prueba
aplicar_razonamiento_rdfs = aplicar_razonador
verificar_casos_inferencia = verificar_tres_casos_inferencia
