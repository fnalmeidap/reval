class TextParser:
    def try_parse(self, byte_buffer: bytes):
        try:
            newline_idx = byte_buffer.find(b'\n')
            if newline_idx != -1:
                line_bytes = byte_buffer[:newline_idx]
                # +1 to consume \n
                return line_bytes, newline_idx + 1
        except Exception:
            pass
            
        return None, 0