import socket
from reval.monitor import MONITORING_SERVER_HOST, MONITORING_SERVER_PORT

port = 1234
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((MONITORING_SERVER_HOST, port))

print(f"Listening on UDP 0.0.0.0:{port}")

while True:
    data, addr = sock.recvfrom(4096)  # max UDP packet size
    msg = data.decode("utf-8")

    print(f"[from {addr}] {msg}")
