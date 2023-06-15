""" IO functions for JSON. """
import json
import os
from pathlib import Path

from modules.errors import report_error_io_read, report_error_io_write
from modules.logger import initialize_logger
from modules.utils import create_directory_if_not_exists

LOGGER = initialize_logger()


def safe_load_json_file(json_path: str) -> dict:
    """ Safely loads a JSON file received as an argument into a dictionary.

    :param json_path: Path to the JSON file to be loaded.
    :type json_path: str
    :return: Dictionary with loaded JSON's data.
    :rtype: dict
    """

    try:
        with open(json_path, "r") as read_file:
            json_data = json.load(read_file)
    except IOError as error:
        file_description = f"input json file"
        report_error_io_read(json_path, file_description, error)

    LOGGER.debug(f"JSON file {json_path} successfully loaded to dictionary.")

    return json_data


def save_json_file(json_data: dict, graph_path: str) -> str:
    """Saves the ontology graph into a file with syntax defined by the user.
    Returns the path in which the json file was saved.

    :param json_data: Dictionary with all data to be saved as a JSON file.
    :type json_data: dict
    :param graph_path: Path to the input graph file.
    :type graph_path: str
    :return: Saved output file path.
    :rtype: str
    """

    # Collecting information for result file name and path
    project_directory = os.getcwd()
    results_directory = "results"
    loaded_file_name = Path(graph_path).stem

    # If directory 'results_directory' not exists, create it
    create_directory_if_not_exists(results_directory, "results directory")

    # Setting file complete path
    output_file_name = loaded_file_name + ".json"
    output_file_path = project_directory + "\\" + results_directory + "\\" + output_file_name

    safe_write_json_file(json_data, output_file_path)

    return output_file_path


def safe_write_json_file(json_data: dict, json_path: str) -> None:
    """ Safely writes a received dictionary as a JSON file in the specified path.

    :param json_data: Dictionary with information to be encoded into JSON.
    :type json_data: dict
    :param json_path: Path in which the JSON file will be saved.
    :type json_path: str
    """

    try:
        with open(json_path, "w") as write_file:
            json.dump(json_data, write_file)
    except IOError as error:
        file_description = f"output json file"
        report_error_io_write(json_path, file_description, error)

    LOGGER.debug(f"Dictionary successfully written as JSON at {json_path}.")
