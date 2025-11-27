import time
from functools import wraps
from .publisher import RevalPublisher


def duration(name: str):
    TO_MILLISECONDS = 1e-6
    """Decorator for measuring execution time of a function."""
    publisher = RevalPublisher.get_instance()

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_ns = time.perf_counter_ns()
            try:
                return func(*args, **kwargs)
            finally:
                end_ns = time.perf_counter_ns()
                duration_ms = (end_ns - start_ns) * TO_MILLISECONDS
                publisher.publish_metric(name, duration_ms)

        return wrapper

    return decorator
