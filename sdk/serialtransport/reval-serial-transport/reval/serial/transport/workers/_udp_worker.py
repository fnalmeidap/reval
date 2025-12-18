class UDPWorker:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def start(self):
        print(f"Starting UDP worker on {self.host}:{self.port}")

    def stop(self):
        print("Stopping UDP worker")