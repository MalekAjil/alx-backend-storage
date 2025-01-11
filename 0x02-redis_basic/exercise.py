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


def call_history(method: Callable) -> Callable:
    """ Decorator to store the history of inputs and outputs for
    a particular function.
    Args:
        method (Callable): The method to be decorated.
    Returns:
        Callable: The decorated method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Wrapper function to store the history of inputs and outputs.
        """
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        # Store input arguments
        self._redis.rpush(input_key, str(args))
        # Execute the original method and store the output
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))
        return output
    return wrapper


class Cache:
    def __init__(self):
        """
        Initialize the Cache class.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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

    def replay(method: Callable):
        """
        Display the history of calls of a particular function.
        Args:
        method (Callable): The method to replay the history for.
        Returns: None
        """
        redis_client = method.__self__._redis
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        inputs = redis_client.lrange(input_key, 0, -1)
        outputs = redis_client.lrange(output_key, 0, -1)
        print(f"{method.__qualname__} was called {len(inputs)} times:")
        for inp, out in zip(inputs, outputs):
            print(f"{method.__qualname__}(*{inp.decode('utf-8')}) -> " +
                  f"{out.decode('utf-8')}")
