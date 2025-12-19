import socket
import threading

_ALL_INTERFACES = "0.0.0.0"
_DEFAULT_MONITORING_SERVER_PORT = 7222

class UdpSocketSingleton:
    _instance = None
    _lock = threading.Lock()
    _target_port = _DEFAULT_MONITORING_SERVER_PORT
    _sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __init__(self):
        pass

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = UdpSocketSingleton()
        return cls._instance
    
    @classmethod
    def set_port(cls, port: int):
        cls._target_port = port

    @classmethod
    def send_metric(cls, bytes_data: bytes):
        print(f"Sending to {_ALL_INTERFACES}:{cls._target_port}")
        cls._sock.sendto(bytes_data, (_ALL_INTERFACES, cls._target_port))
