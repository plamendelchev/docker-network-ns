from .dhclient import DhclientClient

clients = {"dhclient": DhclientClient}


def get_client(name, namespace, interface):
    return clients[name](namespace, interface)
