""" Functions relad to mounting the final dictionary. """
from pprint import pprint

from modules.errors import report_error_requirement_not_met


def get_dictionary_to_be_moved(searched_id: str, list_dictionaries: list[dict]) -> (dict, list[dict]):
    """ Identifies a dictionary to be moved and removes it from the list of dictionaries available.
    If the intended dictionary is not found, an error is reported.

    :param searched_id: ID of the element that will have its dictionary moved.
    :type searched_id: str
    :param list_dictionaries: List of dictionaries being mounted.
    :type list_dictionaries: list[dict]
    :return: tuple where the 1st element is the dictionary to be moved and the 2nd is the updated dictionaries list.
    :rtype: (dict, list[dict])
    """

    # Search dictionary to be moved
    for index, dictionary in enumerate(list_dictionaries):
        if dictionary["id"] == searched_id:
            moved_dictionary = list_dictionaries.pop(index)
            return moved_dictionary, list_dictionaries

    report_error_requirement_not_met("Dictionary not found in the list of dictionaries.")


def substitute_internal_ids(all_ids_list: list[str], list_dictionaries: list[dict]) -> list[dict]:
    """ Identifies internal ids to be substituted, gets the corresponding dictionaries and does the substitution.
    There are four possibilities:
    1. Field is a list and the algorithm must be applied to each element on the list.
    2. Field is a dictionary and the algorithm must be applied to the dictionary.
    3. Conditions met and value substituted.
    4. Conditions not met and no value substituted.

    :param all_ids_list: all ids that can be substituted.
    :type all_ids_list: list[str]
    :param list_dictionaries: List of dictionaries being mounted.
    :type list_dictionaries: list[dict]
    :return: Updated list of dictionaries being mounted (without the moved element).
    :rtype: list[dict]
    """

    replaceable_keys = ["model", "contents"]

    # For each dictionary, verifies if there are values that can be substituted by other dictionaries
    for dictionary in list_dictionaries:
        for key in dictionary.keys():

            # VERIFYING CASE 1: if value is a dictionary
            if type(dictionary[key]) is dict:
                list_dictionaries = substitute_internal_ids(all_ids_list,[dictionary[key]])
            break

            # VERIFYING CASE 1: if value is a dictionary



            # VERIFYING CASES 3 AND 4

            # CONDITION 1: Searched key must not be the own dictionary id
            if key == "id":
                continue
            # CONDITION 2: Value must be an ID of other dictionary
            if dictionary[key] not in all_ids_list:
                continue
            # CONDITION 3: Key must be replaceable
            if key not in replaceable_keys:
                continue

            # VERIFYING CASE3

            # If all conditions are met, get dictionary to be included
            dictionary_to_move, list_dictionaries = get_dictionary_to_be_moved(dictionary[key], list_dictionaries)

            # Moving dictionary
            dictionary[key] = dictionary_to_move.copy()

    return list_dictionaries


def mount_json_dictionary(list_dictionaries: list[dict]) -> dict:
    """ Receives a list with all individual object dictionaries and mount into a single dictionary to be converted
    to JSON.

    :param list_dictionaries: List with all individual object dictionaries.
    :type list_dictionaries: list[dict]
    :return: Single dictionary with all graph's content in a format to be encoded into a JSON file.
    :rtype: dict
    """

    all_ids_list = []

    # Getting list of all available dictionary objects' ids (other than Project)
    for dictionary in list_dictionaries:
        if dictionary['type'] != 'Project':
            all_ids_list.append(dictionary['id'])

    print("before while")
    pprint(list_dictionaries)
    count = 0

    # Iteratively substitute fields with ids as values by whole dictionaries until there is only one left
    while len(list_dictionaries) != 1:
        count += 1
        print(f"\nInside while. Iteration {count}. Size = {len(list_dictionaries)}\n")

        list_dictionaries = substitute_internal_ids(all_ids_list, list_dictionaries)

        if count > 2:
            break

    print("after while")
    pprint(list_dictionaries)

    # The resulting dictionary in the list is going to be the full JSON dictionary
    json_data = list_dictionaries[0].copy()

    return json_data
