MONITORING_SERVER_HOST = "127.0.0.1"
MONITORING_SERVER_PORT = 7222


def setup(host=None, port=None):
    """Update global config values."""
    global MONITORING_SERVER_HOST, MONITORING_SERVER_PORT
    
    if host is not None:
        MONITORING_SERVER_HOST = host
    if port is not None:
        MONITORING_SERVER_PORT = port
