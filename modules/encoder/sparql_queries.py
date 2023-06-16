""" SPARQL queries to be used at the encoding process. """

# Returns individuals IDs and types
QUERY_FUTURE_OBJECTS = """
                        PREFIX ontouml: <https://w3id.org/ontouml#>
                        SELECT DISTINCT ?elem_uri ?elem_type
                        WHERE {
                            ?elem_uri rdf:type ?elem_type .
                        }"""

QUERY_OBJECT_PROPERTIES = """
                            PREFIX ontouml: <https://w3id.org/ontouml#>
                            SELECT DISTINCT ?elem_uri ?elem_type
                            WHERE {
                                ?elem_uri rdf:type ?elem_type .
                            }"""
