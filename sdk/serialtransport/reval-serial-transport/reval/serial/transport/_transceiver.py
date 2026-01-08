import serial
import threading
import logging

from ._eventbus import EventBus, MessageType
from ._logging_config import configure_logging
from .parsers import MAVLinkParser, TextParser, MAVLinkVersion

configure_logging()

logger = logging.getLogger(__name__)

class SerialTransceiver:
    def __init__(self, port = None, baud = 57600, bus: EventBus = None):
        self.port = port
        self.baud = baud
        self.bus = bus
        self.running = False
        self.buffer = bytearray()

        self.ser = serial.Serial(port=self.port, baudrate=self.baud, timeout=0.1)
        self.tx_lock = threading.Lock()

        self.mav_parser = MAVLinkParser()
        self.text_parser = TextParser()

    def start(self):
        if self.port is None or self.bus is None:
            raise ValueError("Please specify both serial port and event bus before starting transceiver.")
        
        self.running = True
        self.thread = threading.Thread(target=self._rx_loop, daemon=True)
        self.thread.start()

    def _rx_loop(self):
        logger.info("SerialTransceiver RX loop started.")
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
                    msg, length = self.text_parser.try_parse(self.buffer)
                    if msg:
                        self.bus.publish(MessageType.TEXT, msg)
                        self.buffer = self.buffer[length:]
                        consumed = True

                if not consumed and len(self.buffer) > 0:
                     if self.buffer[0] not in [MAVLinkVersion.V1, MAVLinkVersion.V2] and self.buffer[0] > 127:
                         self.buffer = self.buffer[1:]
                     elif len(self.buffer) > 2048:
                         self.buffer = self.buffer[1:]
        
        except Exception as e:
            print(f"SerialTransceiver error: {e}")

    def send_text(self, text_msg: str):
        if not text_msg.endswith('\n'):
            text_msg += '\n'

        payload = text_msg.encode('utf-8')
        self.send_raw(payload)

    def send_mavlink(self, msg_bytes: bytes):
        try:
            self.send_raw(msg_bytes)
        except Exception as e:
            print(f"Error packing MAVLink message: {e}")

    def send_raw(self, payload: bytes):
        try:
            with self.tx_lock:
                if self.ser.is_open:
                    self.ser.write(payload)
        except Exception as e:
            print(f"Error sending data: {e}")
