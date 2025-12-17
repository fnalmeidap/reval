import serial
import time

PORT = "/dev/pts/6"
BAUDRATE = 115200

ser = serial.Serial(PORT, BAUDRATE, timeout=1)

print(f"Sending on {PORT}")

while True:
    msg = "Hello over virtual TTY!\n"
    ser.write(msg.encode("utf-8"))
    print(f"Sent: {msg.strip()}")
    time.sleep(1)
