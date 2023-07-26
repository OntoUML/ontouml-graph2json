""" Treatment of specific types of objects. """

from rdflib import Graph, URIRef, RDF

from src.modules.globals import URI_ONTOLOGY, URI_ONTOUML


def count_dictionary_types(list_dictionaries: list[dict]) -> dict:
    """ Counts the different types that occur in the list of dictionaries and their quantity.

    :param list_dictionaries: List with all individual object dictionaries.
    :type list_dictionaries: list[dict]
    :return: Dictionary with types and respective number of occurrences.
    :rtype: dict
    """

    available_types = {}

    for dictionary in list_dictionaries:
        elem_type = dictionary["type"]
        # Counting different types in the generated dictionary
        if elem_type in available_types:
            available_types[elem_type] += 1
        else:
            available_types[elem_type] = 1

    return available_types


def treat_dict_diagram(list_dictionaries: list[dict], ontology_graph: Graph):
    """ Receives a list with all objects as dictionaries and treats specificities of each object of type 'Diagram'.

    :param list_dictionaries: List with all individual object dictionaries.
    :type list_dictionaries: list[dict]
    :param ontology_graph: Graph compliant with the OntoUML Vocabulary loaded from file.
    :type ontology_graph: Graph
    """

    for diagram_dict in list_dictionaries:
        # Treats only objects of type 'Diagram'
        if diagram_dict['type'] != 'Diagram':
            continue

        # Get diagram owner's type
        for owner_type in ontology_graph.objects(URIRef(URI_ONTOLOGY + diagram_dict['owner']), RDF.type):
            got_owner_type = owner_type.toPython().replace(URI_ONTOUML, "")
            diagram_dict['owner'] = {"id": diagram_dict['owner'],
                                     "type": got_owner_type}


def treat_dictionary_types(list_dictionaries: list[dict], ontology_graph: Graph):
    """ Receives a list with all objects in format of dictionary and treats specificities of each object type.

    :param list_dictionaries: List with all individual object dictionaries.
    :type list_dictionaries: list[dict]
    :param ontology_graph: Graph compliant with the OntoUML Vocabulary loaded from file.
    :type ontology_graph: Graph
    """

    available_types = count_dictionary_types(list_dictionaries)

    if "Diagram" in available_types:
        treat_dict_diagram(list_dictionaries, ontology_graph)
