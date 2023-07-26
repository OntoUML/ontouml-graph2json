""" Contains the definitions of the arguments to be provided by the user. Publishes the arguments (as the global
variable ARGUMENTS of type dictionary) to be used in other modules whenever necessary. """

import argparse

from src.modules.globals import METADATA
from src.modules.logger import initialize_logger

LOGGER = initialize_logger()


def treat_user_arguments() -> dict:
    """ Treat arguments provided by the user when starting software execution.

    :return: Dictionary containing all arguments provided by the user.
    :rtype: dict
    """

    about_message = METADATA["name"] + " - version " + METADATA["version"]

    # PARSING ARGUMENTS
    args_parser = argparse.ArgumentParser(prog=METADATA["name"],
                                          description=METADATA["description"] + ". Version: " + METADATA["version"],
                                          allow_abbrev=False,
                                          epilog="More information at: " + METADATA["homepage"])

    args_parser.version = about_message

    # POSITIONAL ARGUMENT
    args_parser.add_argument("graph_file", type=str, action="store",
                             help="The path of the graph file to be encoded.")

    # AUTOMATIC ARGUMENTS
    args_parser.add_argument("-v", "--version", action="version", help="Prints the software version and exits.")

    # Execute arguments parser
    arguments = args_parser.parse_args()

    # Asserting dictionary keys
    arguments_dictionary = {"graph_path": arguments.graph_file}

    LOGGER.debug(f"Arguments parsed. Obtained values are: {arguments_dictionary}.")

    return arguments_dictionary


global ARGUMENTS
ARGUMENTS = treat_user_arguments()
