import time
from reval.serial.transport._transceiver import SerialTransceiver
from reval.serial.transport._eventbus import EventBus, MessageType

from reval.serial.transport import SerialTransceiver
from reval.serial.transport import EventBus, MessageType

bus = EventBus()
transceiver = SerialTransceiver('/dev/pts/7', 115200, bus)

def on_mavlink(msg):
    print(f"[MAVLINK]: {msg}")

def on_text(text):
    print(f"[SARP]: {text}")

bus.subscribe(MessageType.MAVLINK, on_mavlink)
bus.subscribe(MessageType.SARP, on_text)

transceiver.start()

print("Listening for MAVLink and SARP messages...")
while True:
    time.sleep(1)