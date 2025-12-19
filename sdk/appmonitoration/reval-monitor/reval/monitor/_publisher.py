import json
import threading
from .network import UdpSocketSingleton

class RevalPublisher:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        pass

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = RevalPublisher()
        return cls._instance

    def publish_metric(self, name: str, duration_ms: float, metadata: dict = {}):
        duration_data = {}
        duration_data["scope"] = name
        duration_data["duration_ms"] = duration_ms
        duration_data["meta"] = metadata

        json_data = json.dumps(duration_data).encode("utf-8")
        UdpSocketSingleton.send_metric(json_data)
