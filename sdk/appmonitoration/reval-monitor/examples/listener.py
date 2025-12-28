import socket

_ALL_HOST_INTERFACES = "0.0.0.0"

port = 1234
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((_ALL_HOST_INTERFACES, port))

print(f"Listening on UDP {_ALL_HOST_INTERFACES}:{port}")

while True:
    data, addr = sock.recvfrom(4096)  # max UDP packet size
    msg = data.decode("utf-8")

    print(f"[from {addr}] {msg}")
