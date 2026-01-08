import time
from pymavlink import mavutil

def send_over_serial():
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


def send_over_udp():
    UDP_IP = "127.0.0.1"
    UDP_PORT = 14550

    # Open MAVLink connection over UDP (send-only)
    mav = mavutil.mavlink_connection(
        f"udpout:{UDP_IP}:{UDP_PORT}",
        source_system=1,
        source_component=1
    )

    print(f"Sending MAVLink HEARTBEAT to {UDP_IP}:{UDP_PORT}")

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

if __name__ == "__main__":
    send_over_udp()