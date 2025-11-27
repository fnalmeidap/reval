import threading
from .network.udp_socket import UdpSocketSender
from .proto.messages import Duration


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

    def publish_metric(self, name: str, duration_ms: float):
        duration_proto = Duration()
        duration_proto.name = name
        duration_proto.duration_ms = duration_ms
        bytes_data = duration_proto.SerializeToString()
        self.message_sender.send_metric(bytes_data)
