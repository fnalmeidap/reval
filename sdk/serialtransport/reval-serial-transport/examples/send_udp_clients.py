import socket
import threading
import time
import os
import psutil

from pymavlink import mavutil

def bytes_to_mb(value: int) -> float:
    return value / (1024 * 1024)

def mavlink_udp_sender():
    """
    Sends MAVLink HEARTBEAT messages over UDP.
    """
    print("Starting MAVLink UDP sender...")

    mav = mavutil.mavlink_connection(
        "udpout:127.0.0.1:14551"
    )

    # Optional: wait for receiver readiness
    time.sleep(1)

    while True:
        mav.mav.heartbeat_send(
            mavutil.mavlink.MAV_TYPE_GENERIC,
            mavutil.mavlink.MAV_AUTOPILOT_INVALID,
            0,  # base_mode
            0,  # custom_mode
            mavutil.mavlink.MAV_STATE_ACTIVE
        )

        print("[MAVLINK] HEARTBEAT sent")
        time.sleep(1)


def raw_udp_sender():
    """
    Sends a simple raw UDP heartbeat message.
    """
    print("Starting raw UDP sender...")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    target = ("127.0.0.1", 15000)

    while True:
        payload = b"HEARTBEAT"
        sock.sendto(payload, target)

        print("[RAW UDP] HEARTBEAT sent")
        time.sleep(1)


def main():
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    mavlink_thread = threading.Thread(
        target=mavlink_udp_sender,
        daemon=True
    )

    raw_udp_thread = threading.Thread(
        target=raw_udp_sender,
        daemon=True
    )

    mavlink_thread.start()
    raw_udp_thread.start()

    print("Both senders running. Press Ctrl+C to exit.")

    try:
        while True:
            # print(f"PID: {process.pid}")
            # print(f"RSS (Resident Set Size): {bytes_to_mb(memory_info.rss):.2f} MB")
            # print(f"VMS (Virtual Memory Size): {bytes_to_mb(memory_info.vms):.2f} MB")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down.")

if __name__ == "__main__":
    main()
