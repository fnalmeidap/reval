import json
import threading
from .network.udp_socket import UdpSocketSender
from .file.storage import _write_log



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

        json_data = json.dumps(duration_data)
        bytes_data = json_data.encode("utf-8")
        _write_log(f"{json_data}")
        # self.message_sender.send_metric(bytes_data)
