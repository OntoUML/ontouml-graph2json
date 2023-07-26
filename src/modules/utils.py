""" Diverse util and auxiliary functions. """
import os
from datetime import datetime
from pprint import pprint

from modules.errors import report_error_io_write
from modules.logger import initialize_logger

LOGGER = initialize_logger()


def get_date_time(date_time_format: str) -> str:
    """ Return a string with date and time according to the specified format received as argument.
    For valid formats: https://docs.python.org/3.11/library/datetime.html#strftime-and-strptime-format-codes

    :param date_time_format: Valid format accepted by the datetime function.
    :type date_time_format: str
    :return: Formatted current date and time.
    :rtype: str
    """

    now = datetime.now()
    date_time = now.strftime(date_time_format)

    return date_time


def create_directory_if_not_exists(directory_path: str, file_description: str) -> None:
    """ Checks if the directory that has the path received as argument exists.
    If it does, do nothing. If it does not, create it.

    :param directory_path: Path to the directory to be created (if it does not exist).
    :type directory_path: str
    """

    try:
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
    except OSError as error:
        if file_description is None:
            file_description = "directory"
        report_error_io_write(directory_path, file_description, error)


def safe_write_dict_to_txt_file(text_data: dict, txt_path: str) -> None:
    """ Safely writes a received dictionary as a JSON file in the specified path.

    :param json_data: Dictionary with information to be saved as text.
    :type json_data: dict
    :param txt_path: Path in which the txt file will be saved.
    :type txt_path: str
    """

    try:
        with open(txt_path, 'w') as file:
            pprint(text_data, file)
    except IOError as error:
        file_description = f"output txt comparison file"
        report_error_io_write(txt_path, file_description, error)

    LOGGER.debug(f"Dictionary successfully written as TXT at {txt_path}.")
