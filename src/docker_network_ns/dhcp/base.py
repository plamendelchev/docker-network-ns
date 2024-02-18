from pyroute2 import NSPopen


class BaseDhcpClient:
    def __init__(self, namespace, interface):
        self.namespace = namespace
        self.interface = interface

    def run(self, command, **kwargs):
        nsp = NSPopen(self.namespace, command, **kwargs)
        nsp.wait()
        nsp.release()
