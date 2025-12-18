from enum import Enum, auto
from typing import Callable, Dict, List, Any

class MessageType(Enum):
    MAVLINK = auto()
    TEXT = auto()

class EventBus:
    def __init__(self):
        self._subscribers: Dict[MessageType, List[Callable]] = {
            t: [] for t in MessageType
        }

    def subscribe(self, message_type: MessageType, callback: Callable[[Any], None]):
        self._subscribers[message_type].append(callback)

    def publish(self, message_type: MessageType, message: Any) -> None:
        for callback in self._subscribers[message_type]:
            try:
                callback(message)
            except Exception as e:
                print(f"Error in callback for {message_type}: {e}")
