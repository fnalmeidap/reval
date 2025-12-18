import socket
from pymavlink import mavutil
from reval.serial.transport import SerialTransceiver
from reval.serial.transport import EventBus, MessageType

UDP_IP = "0.0.0.0"
UDP_PORT = 14550

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

bus = EventBus()
transceiver = SerialTransceiver('/dev/pts/6', 115200, bus)
mav = mavutil.mavlink.MAVLink(None)

print(f"Listening for UDP packets on {UDP_IP}:{UDP_PORT}")

while True:
    data, addr = sock.recvfrom(4096)
    print(f"\nReceived {len(data)} bytes from {addr}")
    message = mav.parse_buffer(data)
    print(f"Parsed MAVLink messages: {len(message)}")
    print(f"Parsed MAVLink message: {message[0]}")
    transceiver.send_mavlink(data)
