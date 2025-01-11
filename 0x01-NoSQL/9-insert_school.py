#!/usr/bin/env python3
"""Insert School"""


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document in a collection based on kwargs.
    Args:
        mongo_collection: The PyMongo collection object.
        **kwargs: The keyword arguments representing the document fields
        and values.
    Returns:
        The new _id of the inserted document.
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
