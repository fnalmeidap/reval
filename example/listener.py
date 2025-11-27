import socket
from reval import config

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((config.PUBLISHER_HOST, config.PUBLISHER_PORT))

print(f"Listening on UDP {config.PUBLISHER_HOST}:{config.PUBLISHER_PORT}")

while True:
    data, addr = sock.recvfrom(4096)  # max UDP packet size
    msg = data.decode("utf-8")

    print(f"[from {addr}] {msg}")
