from enum import IntEnum
from pymavlink import mavutil

class MAVLinkVersion(IntEnum):
    V1 = 0xFE
    V2 = 0xFD

_MAVLINK_V1_HEADER_CRC_BYTES = 8
_MAVLINK_V2_HEADER_CRC_BYTES = 12
_MAVLINK_SIGNATURE_BYTES = 13
_MAVLINK_INCOMPATIBILITY_FLAG = 0x01


class MAVLinkParser:
    def __init__(self):
        self.mav = mavutil.mavlink.MAVLink(None)

    def _handle_packet_len(self, byte_buffer: bytes, payload_len: int) -> int:
        # Required to determine full packet length based on version and flags
        # Refer to: https://mavlink.io/en/guide/serialization.html
        header = byte_buffer[0]
        incompat_flags = byte_buffer[2]

        if header == MAVLinkVersion.V1:
            return payload_len + _MAVLINK_V1_HEADER_CRC_BYTES
        
        if header == MAVLinkVersion.V2:
            packet_len = payload_len + _MAVLINK_V2_HEADER_CRC_BYTES
            
            if incompat_flags & _MAVLINK_INCOMPATIBILITY_FLAG:
                packet_len += _MAVLINK_SIGNATURE_BYTES
            
            return packet_len

    def try_parse(self, byte_buffer: bytes):
        """
        Returns:
            (parsed_msg, bytes_consumed) if success
            (None, 0) if incomplete data (wait for more)
            (None, -1) if invalid (skip byte)
        """
        if not byte_buffer:
            return None, 0
        
        header = byte_buffer[0]
        if header not in [MAVLinkVersion.V1, MAVLinkVersion.V2]:
            return None, -1
        
        if len(byte_buffer) < 3:
            return None, 0
        
        payload_len = byte_buffer[1]
        packet_len = self._handle_packet_len(byte_buffer, payload_len)

        if len(byte_buffer) < packet_len:
            return None, 0
        
        candidate_data = byte_buffer[:packet_len]

        msgs = self.mav.parse_buffer(candidate_data)

        if msgs:
            return msgs[0], packet_len
        
        return None, -1