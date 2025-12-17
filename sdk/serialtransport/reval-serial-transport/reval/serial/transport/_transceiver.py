import serial
import time
import threading

from ._eventbus import EventBus, MessageType
from .parsers import MAVLinkParser, SARPParser

class SerialTransceiver:
    def __init__(self, port, baud, bus: EventBus):
        self.port = port
        self.baud = baud
        self.bus = bus
        self.running = False
        self.buffer = bytearray()

        self.ser = serial.Serial(port=self.port, baudrate=self.baud, timeout=0.1)
        self.tx_lock = threading.Lock()

        self.mav_parser = MAVLinkParser()
        self.sarp_parser = SARPParser()

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._rx_loop, daemon=True)
        self.thread.start()

    def _rx_loop(self):
        print("SerialTransceiver RX loop started.")
        try:
            while self.running:
                chunk = self.ser.read(128)
                if not chunk:
                    continue

                self.buffer += chunk
                
                print(f"Read {len(chunk)} bytes from serial port. Buffer length now: {len(self.buffer)}")
                consumed = False

                msg, length = self.mav_parser.try_parse(self.buffer)
                if msg:
                    self.bus.publish(MessageType.MAVLINK, msg)
                    self.buffer = self.buffer[length:]
                    consumed = True
                
                if not consumed:
                    msg, length = self.sarp_parser.try_parse(self.buffer)
                    if msg:
                        self.bus.publish(MessageType.SARP, msg)
                        self.buffer = self.buffer[length:]
                        consumed = True

                if not consumed and len(self.buffer) > 0:
                     if self.buffer[0] not in [0xFD, 0xFE] and self.buffer[0] > 127:
                         self.buffer = self.buffer[1:]
                     elif len(self.buffer) > 2048:
                         self.buffer = self.buffer[1:]
        
        except Exception as e:
            print(f"SerialTransceiver error: {e}")

    def send_sarp(self, sarp_msg: str):
        if not sarp_msg.endswith('\n'):
            sarp_msg += '\n'

        payload = sarp_msg.encode('utf-8')
        self.send_raw(payload)

    def send_mavlink(self, msg_obj):
        try:
            payload = msg_obj.pack(self.mav_parser.mav)
            self.send_raw(payload)
        except Exception as e:
            print(f"Error packing MAVLink message: {e}")
            return

    def send_raw(self, payload: bytes):
        try:
            with self.tx_lock:
                if self.ser.is_open:
                    self.ser.write(payload)
        except Exception as e:
            print(f"Error sending data: {e}")