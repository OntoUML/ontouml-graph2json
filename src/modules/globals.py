""" Defines global variables to be used in other modules. Also, publishes the metadata contained in the pyproject.toml
as the global variable METADATA as a dictionary to be used in other modules. """

import toml

# Software's metadata
global METADATA
metadata_project = toml.load("../pyproject.toml")
METADATA = metadata_project["project"]

# URI Information
URI_ONTOLOGY = "https://example.org#"
URI_ONTOUML = "https://w3id.org/ontouml#"
