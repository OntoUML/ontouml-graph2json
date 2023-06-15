""" Argument Treatments """

import argparse

from globals import SOFTWARE_ACRONYM, SOFTWARE_VERSION, SOFTWARE_NAME, SOFTWARE_URL
from modules.logger import initialize_logger

LOGGER = initialize_logger()


def treat_user_arguments() -> str:
    """ Treat arguments provided by the user when starting software execution.

    :return: Path to the graph file to be encoded provided by the user.
    :rtype: str
    """

    LOGGER.debug("Parsing user's arguments...")

    about_message = SOFTWARE_ACRONYM + " - version " + SOFTWARE_VERSION

    # PARSING ARGUMENTS
    arguments_parser = argparse.ArgumentParser(prog=SOFTWARE_ACRONYM,
                                               description=SOFTWARE_NAME + ". Version: " + SOFTWARE_VERSION,
                                               allow_abbrev=False, epilog="More information at: " + SOFTWARE_URL)

    arguments_parser.version = about_message

    # POSITIONAL ARGUMENT
    arguments_parser.add_argument("graph_file", type=str, action="store",
                                  help="The path of the graph file to be encoded.")

    # AUTOMATIC ARGUMENTS
    arguments_parser.add_argument("-v", "--version", action="version", help="Prints the software version and exits.")

    # Execute arguments parser
    arguments = arguments_parser.parse_args()

    # Asserting dictionary keys
    arguments_dictionary = {"graph_path": arguments.graph_file}

    LOGGER.debug(f"Arguments parsed. Obtained values are: {arguments_dictionary}.")

    return arguments_dictionary["graph_path"]
