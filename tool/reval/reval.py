import time
from functools import wraps
from .publisher import RevalPublisher

TO_MILLISECONDS = 1e-6
LATEST_ELEMENT = -1

_metadata_stack = []

def add_metadata(data: dict):
    """Add metadata to the current context."""
    if _metadata_stack:
        _metadata_stack[LATEST_ELEMENT].update(data)

def monitor(name: str):
    """Decorator for measuring execution time of a function."""

    publisher = RevalPublisher.get_instance()

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            metadata = {}
            _metadata_stack.append(metadata)
            
            start_ns = time.perf_counter_ns()
            try:
                return func(*args, **kwargs)
            finally:
                end_ns = time.perf_counter_ns()
                duration_ms = (end_ns - start_ns) * TO_MILLISECONDS
                metadata = _metadata_stack.pop()
                publisher.publish_metric(name, duration_ms, metadata)

        return wrapper

    return decorator
