import json
import threading
from .network.udp_socket import UdpSocketSender

class RevalPublisher:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        self.message_sender = UdpSocketSender.get_instance()

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
        self.message_sender.send_metric(json_data)