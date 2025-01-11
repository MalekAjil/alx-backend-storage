#!/usr/bin/python3
"""Redis"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count how many times a method is called.
    Args:
        method (Callable): The method to be decorated.
    Returns:
        Callable: The decorated method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to increment the count for the method call.
        """
        key = f"{method.__qualname__}"
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    def __init__(self):
        """
        Initialize the Cache class.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using a random key and return the key.
        Args:
            data (Union[str, bytes, int, float]): The data to store in Redis.
        Returns:
            str: The key under which the data is stored.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None
            ) -> Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis and optionally convert it using a callable.
        Args:
         key (str): The key to retrieve from Redis.
         fn (Optional[Callable]): A callable to convert the data back to
         the desired format.
        Returns:
         Union[str, bytes, int, float, None]: The retrieved data,
         optionally converted.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve a string from Redis.
        Args:
          key (str): The key to retrieve from Redis.
        Returns:
          Optional[str]: The retrieved string,
          or None if the key does not exist.
        """
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve an integer from Redis.
        Args:
          key (str): The key to retrieve from Redis.
        Returns:
          Optional[int]: The retrieved integer,
          or None if the key does not exist.
        """
        return self.get(key, int)
