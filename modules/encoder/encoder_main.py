""" Encoding functions for the diverse types of objects that are part of the OntoUML-Schema. """
from rdflib import Graph

from modules.encoder.mount_dictionaries import mount_model_dict, mount_project_dict


def encode_graph_to_json(ontology_graph: Graph) -> dict:
    """ Receives a Graph compliant with the OntoUML Vocabulary and encode it into a
    JSON compliant with the OntoUML-Schema.

    :param ontology_graph: Graph compliant with the OntoUML Vocabulary loaded from file.
    :type ontology_graph: Graph
    :return: JSON compliant with the OntoUML-Schema obtained from the received Graph.
    :rtype: dict
    """

    # Mounting model dictionary
    model_dict = mount_model_dict(ontology_graph)

    # Mounting project dictionary
    project_dict = mount_project_dict(ontology_graph)

    return project_dict
