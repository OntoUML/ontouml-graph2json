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

    object_dictionary = {"id": elem_id,
                         "type": elem_type
                         }

    for s, p, o in ontology_graph.triples((uri_elem_id, None, None)):
        if URI_ONTOUML in p:
            dict_key = p.toPython().replace(URI_ONTOUML, "")
            dict_value = o.toPython().replace(URI_ONTOLOGY, "")
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
        # Getting dictionary properties (FIRST FILL THEN QUERY OR THE OPPOSITE?)
        object_dictionary = create_individual_object_dictionary(uri_elem_id, uri_elem_type, ontology_graph)

        # Complete dictionaries with null values
        elem_type = uri_elem_type.toPython().replace(URI_ONTOUML, "")
        object_dictionary = fill_json_objects(object_dictionary, elem_type)
        list_dictionaries.append(object_dictionary)

    return list_dictionaries


def mount_json_dictionary(list_dictionaries: list[dict]) -> dict:
    """ Receives a list with all individual object dictionaries and mount into a single dictionary to be converted
    to JSON.

    :param list_dictionaries: List with all individual object dictionaries.
    :type list_dictionaries: list[dict]
    :return: Single dictionary with all graph's content in a format to be encoded into a JSON file.
    :rtype: dict
    """

    replaceable_keys = ["model"]
    all_ids_list = []
    json_data = {}

    for dictionary in list_dictionaries:

        # Getting list of all dictionary objects' ids (other than Project)
        if dictionary['type'] != 'Project':
            all_ids_list.append(dictionary['id'])

        # Initializing final dictioinary with Project's dictionary.
        if dictionary['type'] == 'Project':
            json_data = dictionary.copy()

    # For each dictionary, verifies if there are values that can be substituted by other dictionaries
    for inc_dictionary in list_dictionaries:
        for key in inc_dictionary.keys():

            # Replace condition 1: Searched key must not be the own dictionary id
            if key == "id":
                continue

            # Replace condition 2: Value must be an ID of other dictionary
            if inc_dictionary[key] not in all_ids_list:
                continue

            # Replace condition 3: Key must be replaceable
            if key not in replaceable_keys:
                continue

            # If all conditions are met, replace
            json_data[key] = inc_dictionary.copy()

    return json_data
