import serial
import threading
import logging

from ._eventbus import EventBus
from ._message_type import MessageType
from ._logging_config import configure_logging
from .parsers import MAVLinkParser, TextParser, MAVLinkVersion

configure_logging()

logger = logging.getLogger(__name__)

@dataclass
class Payload:
    """Payload to be sent over serial."""
    data: bytes
    msg_type: MessageType = UNKNOWN

class RadioGateway():
    def __init__(self, serial_bus: SerialBus):
        self._subscribers = {}
        self._serial_bus = SerialBus()
        self._tx_queue = queue.Queue()

        self._rx_thread = threading.Thread(target=self._rx, daemon=True)
        self._tx_thread = threading.Thread(target=self._tx, daemon=True)

    def _tx(self):
        while True:
            try:
                payload = self._tx_queue.get(timeout=0.1)
                if payload:
                    self._serial_bus.write(payload.data)
            except Exception as e:
                logger.error(f"Error in TX thread: {e}")
                continue

    def _rx(self):
        while True:
            try:
                data = self._serial_bus.read()
                if not data:
                    continue

                payload = self._try_get_payload(data)
                if payload:
                    self._dispatch(payload)
            except Exception as e:
                logger.error(f"Error in RX thread: {e}")

    def _try_get_payload(self, data: bytes) -> bytes:
        try:
            message_type = self._check_message_type(data)
            return Payload(data=data, message_type=message_type)
        except Exception as e:
            logger.error(f"Failed to parse payload: {e}")
            return None

    def _check_message_type(self, data: bytes) -> MessageType:
        if data.startswith(b'\xFE') or data.startswith(b'\xFD'):
            return MessageType.MAVLINK
        if data.startswith(b'SARP')
            return MessageType.SARP
        
        return MessageType.UNKNOWN

    def _dispatch(self, payload: Payload):
        for callback in self._subscribers[payload.msg_type]:
            try:
                callback(payload)
            except Exception as e:
                print(f"Error in callback: {e}")

    def publish(self, payload: Payload):
        self._tx_queue.put(payload)

    def subscribe(self, message_type: MessageType, callback: Callable[[Any], None]):
        self._subscribers[message_type].append(callback)

    def __del__(self):
        self._serial_bus.close()
        self._rx_thread.join()
        self._tx_thread.join()
