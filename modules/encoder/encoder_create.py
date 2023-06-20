""" Functions that mount dictionaries that will be part of the generated JSON. """

from rdflib import Graph, URIRef

from globals import URI_ONTOUML, URI_ONTOLOGY
from modules.encoder.sparql_queries import QUERY_FUTURE_OBJECTS
from modules.errors import report_error_requirement_not_met


def return_key_pattern(object_type: str) -> list[str]:
    """ Receives an object type and returns the corresponding list of keys.

    :param object_type: Type of object to have its keys returned.
    :type object_type: str
    :return: List of keys for the given object type.
    :rtype: list[str]
    """

    # Individual lists for each object type
    keys_project = ["id", "name", "description", "type", "model", "diagrams"]
    keys_package = ["id", "name", "description", "type", "propertyAssignments", "contents"]

    # General dictionary
    json_keys = {"Project": keys_project, "Package": keys_package}

    # If key not found, report error.
    if object_type not in json_keys.keys():
        report_error_requirement_not_met("Element type not found in list of keys.")

    return json_keys[object_type]


def get_future_objects(ontology_graph: Graph) -> list[(URIRef, URIRef)]:
    """ Queries the ontology_graph to find individuals that will become objects in the JSON.

    :param ontology_graph: Graph compliant with the OntoUML Vocabulary loaded from file.
    :type ontology_graph: Graph
    :return: A list of tuples containing an object's URIRef id and URIRef type that later will become an object.
    :rtype: list[(URIRef, URIRef)]
    """

    list_future_objects = []

    query_future_objects = ontology_graph.query(QUERY_FUTURE_OBJECTS)

    for row in query_future_objects:
        if (URI_ONTOLOGY not in row.elem_uri) or (URI_ONTOUML not in row.elem_type):
            continue
        else:
            future_object = (row.elem_uri, row.elem_type)
            list_future_objects.append(future_object)

    return list_future_objects


def get_json_schema_dict_key(input_dict_key: str) -> str:
    """ Receives a dictionary key obtained form the Graph and returns the corresponding JSON-Schema key.

    :param input_dict_key:
    :type input_dict_key:
    :return:
    :rtype:
    """

    json_schema_key = {"containsModelElement": "contents"}

    if input_dict_key in json_schema_key:
        updated_dict_key = json_schema_key[input_dict_key]
    else:
        updated_dict_key = input_dict_key

    return updated_dict_key


def create_individual_object_dictionary(uri_elem_id: URIRef, uri_elem_type: URIRef, ontology_graph: Graph) -> dict:
    """ Creates a single dictionary with all known data for a given object.
    The known data is queried from the ontology_graph.

    :param uri_elem_id: URI of the object's ID to have its dictionary created.
    :type uri_elem_id: URIRef
    :param uri_elem_type: URI of the object's type to have its dictionary created.
    :type uri_elem_type: URIRef
    :param ontology_graph: Graph compliant with the OntoUML Vocabulary loaded from file.
    :type ontology_graph: Graph
    :return: New object's dictionary with its data.
    :rtype: dict
    """

    elem_id = uri_elem_id.toPython().replace(URI_ONTOLOGY, "")
    elem_type = uri_elem_type.toPython().replace(URI_ONTOUML, "")

    object_dictionary = {"id": elem_id, "type": elem_type}
    json_field_list = ["contents"]

    for s, p, o in ontology_graph.triples((uri_elem_id, None, None)):

        # CONDITION 1: The predicate must be defined in the OntoUML Vocabulary
        if URI_ONTOUML not in p:
            continue

        # CONDITION 2: the object property 'project' is not available in the JSON representation
        if "project" in p.toPython():
            continue

        dict_key = get_json_schema_dict_key(p.toPython().replace(URI_ONTOUML, ""))
        dict_value = o.toPython().replace(URI_ONTOLOGY, "")

        if dict_key in json_field_list:
            object_dictionary[dict_key] = [dict_value]
        else:
            object_dictionary[dict_key] = dict_value

    return object_dictionary


def fill_json_objects(object_dict: dict, object_type: str) -> dict:
    """ Fills objects' keys with null values (None) when they are not available.

    :param object_dict: Object dictionary containing only known data.
    :type object_dict: dict
    :param object_type: Type of the object dictionary.
    :type object_type: str
    :return: Updated object dictionary, now with null (None) values for empty fields.
    :rtype: dict
    """

    keys_list = return_key_pattern(object_type)

    # If the key is not found in the received dictionary, it will receive this new key with value None
    for key in keys_list:
        if key not in object_dict.keys():
            object_dict[key] = None

    return object_dict


def create_data_dictionaries(ontology_graph: Graph) -> list[(dict, str)]:
    """ Create a list of individual data dictionaries for each future JSON object.

    :param ontology_graph: Graph compliant with the OntoUML Vocabulary loaded from file.
    :type ontology_graph: Graph
    :return: List of individual dictionaries to be later filled and mounted.
    :rtype: list[dict]
    """

    list_dictionaries = []

    # Querying elements to become future dictionaries.
    # list_of_future_objects is a list[(URIRef1, URIRef2)], where URIRef1 is the element's ID and URIRef2 is its type.
    list_of_future_objects = get_future_objects(ontology_graph)

    for uri_elem_id, uri_elem_type in list_of_future_objects:
        # Getting dictionary properties
        object_dictionary = create_individual_object_dictionary(uri_elem_id, uri_elem_type, ontology_graph)

        # Complete dictionaries with null values
        elem_type = uri_elem_type.toPython().replace(URI_ONTOUML, "")
        object_dictionary = fill_json_objects(object_dictionary, elem_type)
        list_dictionaries.append(object_dictionary)

    return list_dictionaries
