from pymavlink import mavutil
from reval.serial.transport import SerialTransceiver
from reval.serial.transport import EventBus, MessageType

master = mavutil.mavlink_connection("udp:127.0.0.1:14550")

print("Listening for GUIDED mode heartbeats...")
bus = EventBus()
transceiver = SerialTransceiver('/dev/ttyUSB0', 57600, bus)

while True:
    # msg = master.recv_match(type="HEARTBEAT", blocking=True)
    # if msg is None:
    #     continue

    # # Decode mode string (PX4 / ArduPilot compatible)
    # mode = mavutil.mode_string_v10(msg)

    # if mode == "GUIDED":
    #     print(
    #         f"GUIDED MODE | "
    #         f"sys={msg.get_srcSystem()} "
    #         f"comp={msg.get_srcComponent()}"
    #     )

    # print(f"Type: {msg.get_type()} | Mode: {mode}")

    # transceiver.send_mavlink(msg)
    transceiver.send_sarp("Hello from MAVProxy!")