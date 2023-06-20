""" Encoding functions for the diverse types of objects that are part of the OntoUML-Schema. """

from rdflib import Graph

from modules.encoder.encoder_create import create_data_dictionaries
from modules.encoder.encoder_mount import mount_json_dictionary


def encode_graph_to_json(ontology_graph: Graph) -> dict:
    """ Receives a Graph compliant with the OntoUML Vocabulary and encode it into a
    JSON compliant with the OntoUML-Schema.

    :param ontology_graph: Graph compliant with the OntoUML Vocabulary loaded from file.
    :type ontology_graph: Graph
    :return: JSON compliant with the OntoUML-Schema obtained from the received Graph.
    :rtype: dict
    """

    # Creating a list of individual dictionaries to be later mounted into a single dictionary using the compositions
    list_dictionaries = create_data_dictionaries(ontology_graph)

    # Mount dictionaries into a single dictionary using the compositions
    json_data = mount_json_dictionary(list_dictionaries)

    return json_data
