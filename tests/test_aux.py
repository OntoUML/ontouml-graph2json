""" Auxiliary test functions. """
import glob

from deepdiff import DeepDiff

from modules.utils import safe_write_dict_to_txt_file


def get_test_list() -> list[str]:
    """ Returns a list with all TTL graph files in the test_files folder.

    :return: List with complete path of all TTL files in the test_files folder.
    :rtype: list[str]
    """

    test_files_folder = "test_files/"
    list_test_files = glob.glob(test_files_folder + '*.ttl')
    list_test_files.sort()

    return list_test_files


def save_json_differences(resulting_json_data: dict, expected_json_data: dict, test_name: str) -> None:
    """ Print three files:
        - test*_added.txt: contains elements newly added.
        - test*_removed.txt: contains elements removed.
        - test*_changed.txt: contains elements whose values changed.
    These values always refer from resulting_json_data ('old') to expected_json_data ('new').

    :param resulting_json_data: Generated resulting JSON data as a dictionary.
    :type resulting_json_data: dict
    :param expected_json_data: Expected JSON data as a dictionary.
    :type expected_json_data: dict
    :param test_name: Name of the test to be used for printing comparison if evaluation result is negative.
    :type test_name: str
    """

    diff_result = DeepDiff(resulting_json_data, expected_json_data, ignore_order=True)
    diff_result_dict = diff_result.to_dict()

    base_path = "results/"
    safe_write_dict_to_txt_file(diff_result_dict, base_path + test_name + "_diff.txt")


def compare_json_files_data(resulting_json_data: dict, expected_json_data: dict, test_name: str) -> bool:
    """ Verifies if resulting JSON data corresponds to expected JSON data.

    :param resulting_json_data: Generated resulting JSON data as a dictionary.
    :type resulting_json_data: dict
    :param expected_json_data: Expected JSON data as a dictionary.
    :type expected_json_data: dict
    :param test_name: Name of the test to be used for printing comparison if evaluation result is negative.
    :type test_name: str
    :return: Boolean value indicating if the resulting and expected JSON data are equal.
    :rtype: bool
    """

    is_equal = (resulting_json_data == expected_json_data)

    if not is_equal:
        save_json_differences(resulting_json_data, expected_json_data, test_name)

    return is_equal
