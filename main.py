""" Main file for encoding a graph into a OntoUML-Schema JSON. """

import time

from modules.arguments import treat_user_arguments
from modules.io_graph import safe_write_json_file
from modules.logger import initialize_logger
from modules.utils import get_date_time, load_all_graph_safely


def ontouml_graph2json(graph_file_path: str, execution_mode: str = "production") -> dict:
    """ Main function for ontouml-graph2json.

    :param graph_file_path: Path to the Graph file to be encoded, provided by the user.
    :type graph_file_path: str
    :param execution_mode: Information about execution mode. Valid values are 'production' (default) and 'test'.
    :type execution_mode: str
    :return: Generated output dictionary that is going to be saved in JSON format. Used for testing.
    :rtype: dict
    """

    logger = initialize_logger(execution_mode)

    if execution_mode == "production":
        # Initial time information
        time_screen_format = "%d-%m-%Y %H:%M:%S"
        start_date_time = get_date_time(time_screen_format)
        st = time.perf_counter()

        logger.info(f"OntoUML Graph2JSON encoder started on {start_date_time}!")

    # Load Graph
    ontology_graph = load_all_graph_safely(graph_file_path)

    # Encode Graph into JSON dictionary
    # TBD

    if execution_mode == "production":
        # Get software's execution conclusion time
        end_date_time = get_date_time(time_screen_format)
        et = time.perf_counter()
        elapsed_time = round((et - st), 3)

        logger.info(f"Encoding concluded on {end_date_time}. Total execution time: {elapsed_time} seconds.")

    # Save JSON file
    output_file_path = safe_write_json_file(json_data, json_path)
    logger.info(f"Output JSON file successfully saved at {output_file_path}.")

    return output_file_path

    # return json_dict


if __name__ == '__main__':
    # Treat arguments
    graph_path = treat_user_arguments()

    # Execute
    ontouml_graph2json(graph_path, "production")
