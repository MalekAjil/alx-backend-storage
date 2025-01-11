#!/usr/bin/env python3
""" Schools By Topic"""


def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of schools having a specific topic.

    Args:
        mongo_collection: The PyMongo collection object.
        topic (string): The topic to search for.

    Returns:
        A list of schools that have the specified topic.
    """
    return list(mongo_collection.find({"topics": topic}))
