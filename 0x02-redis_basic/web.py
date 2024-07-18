#!/usr/bin/env python3
"""
Web caching module
"""
import redis
import requests
from typing import Callable

# Initialize Redis client
r = redis.Redis()

def count_calls(method: Callable) -> Callable:
    """Decorator to count the number of calls to a method"""
    def wrapper(*args, **kwargs):
        """Wrapper function to increment the count and call the original method"""
        url = args[0]
        r.incr(f"count:{url}")
        return method(*args, **kwargs)
    return wrapper

def cache_result(method: Callable) -> Callable:
    """Decorator to cache the result of a method with an expiration time"""
    def wrapper(*args, **kwargs):
        """Wrapper function to cache result and call the original method"""
        url = args[0]
        cached_result = r.get(url)
        if cached_result:
            return cached_result.decode('utf-8')
        result = method(*args, **kwargs)
        r.setex(url, 10, result)
        return result
    return wrapper

@count_calls
@cache_result
def get_page(url: str) -> str:
    """Get the HTML content of a URL and cache it with an expiration time"""
    response = requests.get(url)
    return response.text

if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/3000/url/http://www.example.com"
    print(get_page(url))
    print(f"Access count: {r.get(f'count:{url}').decode('utf-8')}")
    # Wait and try again to see if caching works
    import time
    time.sleep(5)
    print(get_page(url))
    print(f"Access count: {r.get(f'count:{url}').decode('utf-8')}")
    time.sleep(6)
    print(get_page(url))
    print(f"Access count: {r.get(f'count:{url}').decode('utf-8')}")
