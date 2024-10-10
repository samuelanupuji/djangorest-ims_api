from django.core.cache import cache
from functools import wraps


def cache_response(cache_key,timeout=3600):
    def decorator(func):
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            cached_data=cache.get(cache_key)
            if cached_data:
                return cached_data
            response= func(*args, **kwargs)
            cache.set(cache_key, response, timeout=timeout)
            return response
        return wrapped_func
    return decorator