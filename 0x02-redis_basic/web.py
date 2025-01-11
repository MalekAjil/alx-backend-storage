#!/usr/bin/env python3
"""Web Module"""

import requests
import redis
from typing import Callable


redis_client = redis.Redis()


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count how many times a method is called.
    Args:
        method (Callable): The method to be decorated.
    Returns:
        Callable: The decorated method.
    """
    def wrapper(*args, **kwargs):
        """
        Wrapper function to increment the count for the method call.
        """
        url = args[0]
        redis_client.incr(f"count:{url}")
        return method(*args, **kwargs)
    return wrapper


def cache_result(method: Callable) -> Callable:
    """
    Decorator to cache the result of a method call.
    Args:
        method (Callable): The method to be decorated.
    Returns:
        Callable: The decorated method.
    """
    def wrapper(*args, **kwargs):
        """
        Wrapper function to cache the result of the method call.
        """
        url = args[0]
        cached_result = redis_client.get(url)
        if cached_result:
            return cached_result.decode('utf-8')
        result = method(*args, **kwargs)
        redis_client.setex(url, 10, result)
        return result
    return wrapper


@count_calls
@cache_result
def get_page(url: str) -> str:
    """
    Get the HTML content of a URL.
    Args:
        url (str): The URL to fetch.
    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text


# Example usage
if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk"
    print(get_page(url))
    print(get_page(url))
