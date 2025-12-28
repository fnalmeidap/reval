import threading
import pymavlink
import socket
import time
from pymavlink import mavutil
import psutil
import os
import time

def mavlink_udp_client():
    """
    Listens for MAVLink messages over UDP.
    """
    print("Starting MAVLink UDP client...")

    mav = mavutil.mavlink_connection(
        "udp:127.0.0.1:14551",
        autoreconnect=True
    )

    while True:
        msg = mav.recv_match(blocking=True, timeout=1)
        if msg is not None:
            print(f"[MAVLINK] {msg.get_type()}: {msg}")


def raw_udp_client():
    """
    Listens for raw UDP packets.
    """
    print("Starting raw UDP client...")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 15000))

    while True:
        data, addr = sock.recvfrom(4096)
        print(f"[RAW UDP] {len(data)} bytes from {addr}: {data}")

def bytes_to_mb(value: int) -> float:
    return value / (1024 * 1024)

def main():
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()

    mavlink_thread = threading.Thread(
        target=mavlink_udp_client,
        daemon=True,
        name="MAVLinkUDPClient"
    )

    raw_udp_thread = threading.Thread(
        target=raw_udp_client,
        daemon=True,
        name="RawUDPClient"
    )

    # mavlink_thread.start()
    raw_udp_thread.start()

    print("Both UDP clients running. Press Ctrl+C to exit.")

    try:
        while True:
            print(f"PID: {process.pid}")
            print(f"RSS (Resident Set Size): {bytes_to_mb(memory_info.rss):.2f} MB")
            print(f"VMS (Virtual Memory Size): {bytes_to_mb(memory_info.vms):.2f} MB")
            time.sleep(1.0)
    except KeyboardInterrupt:
        print("Shutting down.")


if __name__ == "__main__":
    main()
