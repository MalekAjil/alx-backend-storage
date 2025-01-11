#!/usr/bin/env python3
""" Update Topics Module"""


def update_topics(mongo_collection, name, topics):
    """
    Changes all topics of a school document based on the name.
    
    Args:
        mongo_collection: The PyMongo collection object.
        name (string): The school name to update.
        topics (list of strings): The list of topics approached in the school.
    
    Returns:
        None
    """
    mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
