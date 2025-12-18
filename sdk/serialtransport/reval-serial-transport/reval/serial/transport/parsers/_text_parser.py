class TextParser:
    def try_parse(self, byte_buffer: bytes):
        try:
            newline_idx = byte_buffer.find(b'\n')
            if newline_idx != -1:
                line_bytes = byte_buffer[:newline_idx]
                try:
                    text_msg = line_bytes.decode('utf-8')
                    if text_msg.isprintable():
                        # +1 to consume \n
                        return text_msg, newline_idx + 1
                except UnicodeDecodeError:
                    pass
        except Exception:
            pass
            
        return None, 0