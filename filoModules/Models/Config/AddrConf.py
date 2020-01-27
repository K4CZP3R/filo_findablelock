class AddrConf(object):
    def __init__(self, address, port):
        self.address = address
        self.port = port
    def get_connected(self) -> str:
        return f"{self.address}:{self.port}"