from filoModules.Models.Config.AddrConf import AddrConf

class EmailConf(object):
    def __init__(self, address: AddrConf, sender_mail, password):
        self.server = address.address
        self.port = address.port
        self.sender_mail = sender_mail
        self.password = password