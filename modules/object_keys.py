""" OntoUML-Schema Object keys"""


def return_key_pattern(object_type: str) -> list[str]:
    """ Receives an object type and returns the corresponding list of keys.

    :param object_type: Type of object to have its keys returned.
    :type object_type: str
    :return: List of keys for the given object type.
    :rtype: list[str]
    """

    # Individual lists for each object type
    keys_project = ["id", "name", "description", "type", "model", "diagrams"]
    keys_model = ["id", "name", "description", "type", "propertyAssignments", "contents"]

    # General dictionary
    json_keys = {"project": keys_project, "model": keys_model}

    return json_keys[object_type]
