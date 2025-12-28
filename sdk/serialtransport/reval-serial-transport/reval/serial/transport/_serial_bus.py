import threading
import queue
import serial

class SerialBus:
    def __init__(self, port="/dev/ttyUSB0", baudrate=57600):
        super().__init__(daemon=True)
        self._serial = serial.Serial(port, baudrate, timeout=0)

    def write(self, data: bytes):
        try:
            self._serial.write(data)
        except Exception as e:
            print(f"Error writing to SerialBus: {e}")

    def read(self, size=4096) -> bytes:
        try:
            return self._serial.read(size)
        except Exception as e:
            print(f"Error reading from SerialBus: {e}")
            return b""

    def __del__(self):
        if self._serial.is_open:
            self._serial.close()
        if self.is_alive():
            self.join()
