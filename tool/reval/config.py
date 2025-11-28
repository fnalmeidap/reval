PUBLISHER_HOST = "127.0.0.1"
PUBLISHER_PORT = 7222
ENABLED = True


def setup(host=None, port=None, enabled=None):
    """Update global config values."""
    global PUBLISHER_HOST, PUBLISHER_PORT, ENABLED

    if host is not None:
        PUBLISHER_HOST = host
    if port is not None:
        PUBLISHER_PORT = port
    if enabled is not None:
        ENABLED = enabled
