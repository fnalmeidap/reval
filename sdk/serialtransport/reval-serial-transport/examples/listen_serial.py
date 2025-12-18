import time
from pymavlink import mavutil
from reval.serial.transport._transceiver import SerialTransceiver
from reval.serial.transport._eventbus import EventBus, MessageType

from reval.serial.transport import SerialTransceiver
from reval.serial.transport import EventBus, MessageType

bus = EventBus()
transceiver = SerialTransceiver('/dev/pts/10', 115200, bus)
mav = mavutil.mavlink.MAVLink(None)

def on_mavlink(msg):
    print(f"\nReceived {len(msg)} bytes of MAVLink data")
    message = mav.parse_buffer(msg)
    print(f"Parsed MAVLink messages: {len(message)}")
    print(f"Parsed MAVLink message: {message[0]}")
    print(f"[MAVLINK]: {msg}")

def on_text(text):
    print(f"[SARP]: {text}")

bus.subscribe(MessageType.MAVLINK, on_mavlink)
bus.subscribe(MessageType.SARP, on_text)

transceiver.start()

print("Listening for MAVLink and SARP messages...")
while True:
    time.sleep(1)