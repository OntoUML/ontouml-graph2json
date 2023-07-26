""" IO functions for graphs. """

import os
from pathlib import Path

from modules.errors import report_error_io_read, report_error_io_write
from modules.logger import initialize_logger
from rdflib import Graph

LOGGER = initialize_logger()


def load_all_graph_safely(ontology_file: str) -> Graph:
    """ Safely load graph from file to working memory.

    :param ontology_file: Path to the ontology file to be loaded into the working memory.
    :type ontology_file: str
    :return: RDFLib graph loaded as object.
    :rtype: Graph
    """

    ontology_graph = Graph()

    try:
        ontology_graph.parse(ontology_file, encoding='utf-8')
    except OSError as error:
        file_description = f"input ontology file"
        report_error_io_read(ontology_file, file_description, error)

    LOGGER.info(f"Ontology file {ontology_file} successfully loaded to working memory.")

    return ontology_graph


def save_graph_file(ontouml_graph: Graph, json_path: str, graph_format: str) -> str:
    """Saves the ontology graph into a file with syntax defined by the user.

    :param ontouml_graph: Graph compliant with the OntoUML Vocabulary.
    :type ontouml_graph: Graph
    :param end_date_time_file: String containing the software's execution end date and time.
    :type end_date_time_file: str
    :param json_path: Path to the input json file.
    :type json_path: str
    :param graph_format: Syntax selected by the user to save the graph.
    :type graph_format: str
    :return: Saved output file path.
    :rtype: str
    """

    # Collecting information for result file name and path
    project_directory = os.getcwd()
    results_directory = "results"
    loaded_file_name = Path(json_path).stem

    # If directory 'results_directory' not exists, create it
    create_directory_if_not_exists(results_directory, "results directory")

    # Setting file complete path
    output_file_name = loaded_file_name + "." + graph_format
    output_file_path = project_directory + "\\" + results_directory + "\\" + output_file_name

    safe_write_graph_file(ontouml_graph, output_file_path, graph_format)

    return output_file_path


def safe_write_graph_file(ontouml_graph: Graph, output_file_name: str, syntax: str) -> None:
    """ Safely saves the graph into a file in the informed destination with the desired syntax.

    :param ontouml_graph: Graph compliant with the OntoUML Vocabulary.
    :type ontouml_graph: Graph
    :param output_file_name: Created output file name.
    :type output_file_name: str
    :param syntax: Syntax to be used for saving the ontology file.
    :type syntax: str
    """

    try:
        ontouml_graph.serialize(destination=output_file_name, encoding='utf-8', format=syntax)
    except OSError as error:
        file_description = f"output graph file"
        report_error_io_write(output_file_name, file_description, error)
