import threading
import time
import json
from functools import wraps
from .publisher import RevalPublisher

_local = threading.local()
TO_MILLISECONDS = 1e-6


def monitor(name: str):
    """Decorator for measuring execution time of a function."""

    publisher = RevalPublisher.get_instance()

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            clear_metadata()
            start_ns = time.perf_counter_ns()
            try:
                return func(*args, **kwargs)
            finally:
                end_ns = time.perf_counter_ns()
                duration_ms = (end_ns - start_ns) * TO_MILLISECONDS
                publisher.publish_metric(name, duration_ms, get_metadata())

        return wrapper

    return decorator


def add_metadata(data: dict):
    """Add metadata to the current thread's context. The input will overwrite existing metadata."""
    if not hasattr(_local, "meta"):
        _local.meta = {}
    _local.meta.update(data)


def get_metadata() -> dict:
    """Retrieve metadata for the current thread's context."""
    return getattr(_local, "meta", None)


def clear_metadata():
    """Clear metadata for the current thread's context."""
    if hasattr(_local, "meta"):
        _local.meta = {}
