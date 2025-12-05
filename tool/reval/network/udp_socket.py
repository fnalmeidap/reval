import socket
import threading
from reval import settings


class UdpSocketSender:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.addr = (settings.MONITORING_SERVER_HOST, settings.MONITORING_SERVER_PORT)
        print(f"UDP Socket Sender initialized to {self.addr}")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = UdpSocketSender()
        return cls._instance

    def send_metric(self, bytes_data: bytes):
        self.sock.sendto(bytes_data, self.addr)
