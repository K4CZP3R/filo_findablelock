from filoModules.Models.Config.AddrConf import AddrConf

class MongoConfig(object):
    def __init__(self, address: AddrConf):
        self.server = address.address
        self.port = address.port
    def get_url(self) -> str:
        return f"mongodb://{self.server}:{self.port}/"