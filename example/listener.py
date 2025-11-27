import socket
from reval import config
from reval.proto.generated.metrics_pb2 import Duration

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((config.PUBLISHER_HOST, config.PUBLISHER_PORT))

print(f"Listening on UDP {config.PUBLISHER_HOST}:{config.PUBLISHER_PORT}")

while True:
    data, addr = sock.recvfrom(4096)  # max UDP packet size
    msg = Duration()
    msg.ParseFromString(data)

    print(f"[from {addr}] name={msg.name} duration_ms={msg.duration_ms}")
