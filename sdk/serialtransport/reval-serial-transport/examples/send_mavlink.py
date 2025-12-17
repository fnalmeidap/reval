import time
from pymavlink import mavutil

PORT = "/dev/pts/6"
BAUD = 115200

# Open MAVLink connection over serial
mav = mavutil.mavlink_connection(
    PORT,
    baud=BAUD,
    source_system=1,
    source_component=1
)

print(f"Sending MAVLink HEARTBEAT on {PORT}")

while True:
    mav.mav.heartbeat_send(
        mavutil.mavlink.MAV_TYPE_GENERIC,
        mavutil.mavlink.MAV_AUTOPILOT_INVALID,
        0,  # base_mode
        0,  # custom_mode
        mavutil.mavlink.MAV_STATE_ACTIVE
    )

    print("Sent HEARTBEAT")
    time.sleep(1)
