#!/usr/bin/env python3

import requests
import redis
from functools import wraps
from typing import Callable

# Initialize Redis connection
r = redis.Redis()

def cache_page(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(url: str) -> str:
        # Increment the count of URL accesses
        count_key = f"count:{url}"
        r.incr(count_key)
        
        # Check if the URL content is already cached
        cached_page = r.get(url)
        if cached_page:
            return cached_page.decode('utf-8')
        
        # Fetch the page content using the original function
        page_content = func(url)
        
        # Cache the page content with an expiration of 10 seconds
        r.setex(url, 10, page_content)
        
        return page_content
    return wrapper

@cache_page
def get_page(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    return response.text

if __name__ == "__main__":
    # Example usage
    url = "http://slowwly.robertomurray.co.uk"
    print(get_page(url))
