""" Functions relad to mounting the final dictionary. """

from modules.errors import report_error_requirement_not_met


def copy_dictionary_from_id(element_id: str, list_dictionaries: list[dict]) -> dict:
    """ From a given ID, returns a copy of its corresponding dictionary from the list of dictionaries.
    This operation does not remove the dictionary from the list of dictionaries.
    If ID not found, calls error function.

    :param element_id: ID of the object to have its dictionary to be returned.
    :type element_id: str
    :param list_dictionaries: List of all available dictionaries.
    :type list_dictionaries: list[dict]
    :return: Dictionary that has the element_id as its ID.
    :rtype: dict
    """

    for dictionary in list_dictionaries:
        if dictionary['id'] == element_id:
            copied_dictionary = dictionary.copy()
            return copied_dictionary

    report_error_requirement_not_met(f"ID {element_id} not found in dictionary list.")


def replace_id_pointer_in_dictionary(current_dictionary: dict, element_id: str, element_dict: dict) -> None:
    """ Runs through all the dictionary and search for pointers to the informed ID (element_id). If found, replaces the
    pointer to the whole dictionary that has element_id as its ID (element_dict).

    :param current_dictionary: Dictionary that is going to be searched for pointers to element_id.
    :type current_dictionary: dict
    :param element_id: ID to be searched inside the dictionary.
    :type element_id: str
    :param element_dict: Dictionary that has element_id as its ID.
    :type element_dict: dict
    """

    for key in current_dictionary.keys():

        # Do not search in ID field
        if key == 'id':
            continue

        # If found, substitute
        if current_dictionary[key] == element_id:
            current_dictionary[key] = element_dict.copy()
            break

        # If is list, treat each element
        if type(current_dictionary[key]) is list:
            for item in current_dictionary[key]:
                if item == element_id:
                    current_dictionary[key].remove(item)
                    current_dictionary[key].append(element_dict.copy())

        # Execute recursively if field is a dictionary:
        if type(current_dictionary[key]) is dict:
            replace_id_pointer_in_dictionary(current_dictionary[key], element_id, element_dict)


def mount_json_dictionary(list_dictionaries: list[dict]) -> dict:
    """ Receives a list with all individual object dictionaries and mount into a single dictionary to be converted
    to JSON.

    :param list_dictionaries: List with all individual object dictionaries.
    :type list_dictionaries: list[dict]
    :return: Single dictionary with all graph's content in a format to be encoded into a JSON file.
    :rtype: dict
    """

    list_all_ids = []

    # Get list of all IDs from all dictionaries
    for dictionary in list_dictionaries:
        list_all_ids.append(dictionary["id"])

    # For the rare cases when there is no Project
    json_dictionary = list_dictionaries[0].copy()

    # Get correct upper level dictionary if there is a Project
    for dictionary in list_dictionaries:
        if dictionary['type'] == 'Project':
            json_dictionary = dictionary.copy()
            break

    for element_id in list_all_ids:

        # Getting the corresponding dictionary
        element_dict = copy_dictionary_from_id(element_id, list_dictionaries)

        # Do not treat the same dictionary
        if json_dictionary['id'] == element_dict['id']:
            continue

        # Replace all possible occurrences of the ID in the current dictionary
        replace_id_pointer_in_dictionary(json_dictionary, element_id, element_dict)

    return json_dictionary
