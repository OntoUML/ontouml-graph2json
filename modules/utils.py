""" Diverse util and auxiliary functions. """
import os
from datetime import datetime

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
