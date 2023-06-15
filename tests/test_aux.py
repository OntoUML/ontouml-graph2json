""" Auxiliary test functions. """
import glob

import DeepDiff as DeepDiff

from modules.io_json import safe_write_json_file


def get_test_list() -> list[str]:
    """ Returns a list with all TTL graph files in the test_files folder.

    :return: List with complete path of all TTL files in the test_files folder.
    :rtype: list[str]
    """

    test_files_folder = "test_files/"
    list_test_files = glob.glob(test_files_folder + '*.ttl')
    list_test_files.sort()

    return list_test_files


def print_json_differences(resulting_json_data: dict, expected_json_data: dict) -> None:
    """ Print three files:
        - test_added.txt: contains elements newly added.
        - test_removed.txt: contains elements removed.
        - test_changed.txt: contains elements whose values changed.
    These values always refer from resulting_json_data ('old') to expected_json_data ('new').

    :param resulting_json_data: Generated resulting JSON data as a dictionary.
    :type resulting_json_data: dict
    :param expected_json_data: Expected JSON data as a dictionary.
    :type expected_json_data: dict
    """

    diff_result = DeepDiff(resulting_json_data, expected_json_data)

    # TODO (@pedropaulofb): This must be fixed. Use a relative path instead.
    base_path = "C:\\Users\\PFavatoBarcelos\\Dev\\Work\\ontouml-graph2json\\tests\\test_files\\"

    safe_write_json_file(diff_result["dictionary_item_added"], base_path + "test_added.txt")
    safe_write_json_file(diff_result["dictionary_item_removed"], base_path + "test_removed.txt")
    safe_write_json_file(diff_result["dictionary_values_changed"], base_path + "test_changed.txt")


def compare_json_files_data(resulting_json_data: dict, expected_json_data: dict) -> bool:
    """ Verifies if resulting JSON data corresponds to expected JSON data.

    :param resulting_json_data: Generated resulting JSON data as a dictionary.
    :type resulting_json_data: dict
    :param expected_json_data: Expected JSON data as a dictionary.
    :type expected_json_data: dict
    :return: Boolean value indicating if the resulting and expected JSON data are equal.
    :rtype: bool
    """

    is_equal = (resulting_json_data == expected_json_data)

    if not is_equal:
        print_json_differences(resulting_json_data, expected_json_data)

    return is_equal
