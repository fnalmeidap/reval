import socket

LISTEN_IP = "0.0.0.0"
LISTEN_PORT = 14560   # must match MAVProxy --out port

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((LISTEN_IP, LISTEN_PORT))

from reval.serial.transport import SerialTransceiver
from reval.serial.transport import EventBus, MessageType

bus = EventBus()
transceiver = SerialTransceiver('/dev/ttyUSB0', 57600, bus)

print(f"Listening for MAVLink UDP packets on {LISTEN_IP}:{LISTEN_PORT}")

while True:
    data, addr = sock.recvfrom(4096)
    
    print(f"Received {len(data)} bytes from {addr}")
