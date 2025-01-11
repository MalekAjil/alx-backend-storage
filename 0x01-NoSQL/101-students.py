#!/usr/bin/env python3
""" Top Students"""


def top_students(mongo_collection):
    """
    Returns all students sorted by average score.
    Args:
      mongo_collection: The PyMongo collection object.
    Returns:
      A list of students sorted by average score, each with an 'averageScore' key.
    """
    pipeline = [
        {
            "$project": {
                "name": 1,
                "topics": 1,
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {
            "$sort": {"averageScore": -1}
        }
    ]
    return list(mongo_collection.aggregate(pipeline))
