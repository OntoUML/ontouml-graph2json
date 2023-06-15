""" Main test function. """
from pathlib import Path

import pytest
from tests.test_aux import get_test_list, compare_json_files_data

from main import ontouml_graph2json
from modules.io_json import safe_load_json_file

LIST_OF_TESTS = get_test_list()


@pytest.mark.parametrize("input_file", LIST_OF_TESTS)
def test_ontouml_graph2json(input_file: str) -> None:
    """ Main function for testing the OntoUML Graph2JSON software.

    The test is based on the comparison of the generated JSON data (from a graph file provided in the test folder)
    with a expected resulting JSON (also provided in the test folder).

    :param input_file: Path to the graph file to be tested.
    :type input_file: str
    """

    test_name = Path(input_file).stem

    # Create resulting JSON dictionary
    resulting_json_data = ontouml_graph2json(input_file, "test")

    # Getting expected result
    expected_json_file = input_file.replace(".json", ".ttl")
    resulting_json_data = safe_load_json_file(expected_json_file)

    # Comparing resulting and expected graphs
    is_equal = compare_json_files_data(resulting_json_data, resulting_json_data, test_name)

    assert is_equal
