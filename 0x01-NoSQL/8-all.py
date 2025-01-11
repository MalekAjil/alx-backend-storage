#!/usr/bin/env python3
"""List All Module"""


def list_all(mongo_collection):
    """
    Lists all documents in a collection.
    Args:
        mongo_collection: The PyMongo collection object.
    Returns:
        A list of documents in the collection, or an empty list if 
        no documents are found.
    """
    documents = mongo_collection.find()
    return list(documents) if documents.count() > 0 else []
