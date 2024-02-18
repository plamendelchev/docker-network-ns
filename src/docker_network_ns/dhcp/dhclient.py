from subprocess import DEVNULL

from .base import BaseDhcpClient


class DhclientClient(BaseDhcpClient):
    def start(self):
        super().run(
            command=[
                "dhclient",
                "-nw",
                "-pf",
                f"/run/dhclient-{self.namespace}.pid",
                "-lf",
                f"/var/lib/dhclient/dhclient-{self.namespace}.leases",
                self.interface,
            ],
            stderr=DEVNULL,
        )

    def stop(self):
        super().run(
            command=[
                "dhclient",
                "-r",
                "-pf",
                f"/run/dhclient-{self.namespace}.pid",
                "-lf",
                f"/var/lib/dhclient/dhclient-{self.namespace}.leases",
                self.interface,
            ],
            stderr=DEVNULL,
        )
