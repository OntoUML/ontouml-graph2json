""" Functions that mount dictionaries that will be part of the generated JSON. """
from rdflib import Graph

from modules.object_keys import return_key_pattern


def mount_model_dict(ontology_graph: Graph) -> dict:
    """

    :param ontology_graph:
    :type ontology_graph:
    """

    model_dict = {}
    fill_json_objects(model_dict, "model")
    return model_dict


def mount_project_dict(ontology_graph: Graph, model_dict: dict) -> dict:
    """

    :param ontology_graph:
    :type ontology_graph:
    :param model_dict:
    :type model_dict:
    """

    project_dict = {}
    fill_json_objects(project_dict, "project")
    return project_dict


def fill_json_objects(object_dict: dict, object_type: str) -> dict:
    """ Fills objects' keys with null values when they are not available.

    :param object_dict:
    :type object_dict:
    :param object_type:
    :type object_type:
    """

    keys_list = return_key_pattern(object_type)

    # If the key is not found in the received dictionary, it will receive this new key with value None
    for key in keys_list:
        if key not in object_dict.keys():
            object_dict[key] = None

    return object_dict
