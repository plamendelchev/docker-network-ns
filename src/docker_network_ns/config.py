import json
import re
from dataclasses import dataclass
from json.decoder import JSONDecodeError
from shutil import which

from schema import And, Optional, Or, Schema, SchemaError, SchemaWrongKeyError

from docker_network_ns import constants, dhcp, errors


def validate_mac_address(mac_address):
    match = re.fullmatch(
        r"([0-9A-F]{2}[:]){5}[0-9A-F]{2}|" r"([0-9A-F]{2}[-]){5}[0-9A-F]{2}",
        string=mac_address,
        flags=re.IGNORECASE,
    )
    return True if match else False


default_config = {
    "namespace": "docker",
    "interface": {"name": "docker", "link": "enp2s0", "mac_address": "auto"},
    "ip_address": {"mode": "dhcp", "dhcp_client": "dhclient"},
}

config_schema = Schema(
    {
        Optional("namespace", default=default_config["namespace"]): str,
        Optional("interface", default=default_config["interface"]): {
            "name": str,
            "parent": str,
            "mac_address": Or(
                "auto",
                validate_mac_address,
                error="Invalid MAC Address - should be either 'auto' or a valid MAC Address",
            ),
        },
        Optional("ip_address", default=default_config["ip_address"]): Or(
            {
                "mode": "dhcp",
                "dhcp_client": And(
                    str,
                    lambda c: c in dhcp.clients,
                    which,
                    error="Invalid DHCP Client - either not support or not installed on the system",
                ),
            },
            {"mode": "static", "address": str},
            only_one=True,
        ),
    }
)


@dataclass
class Config:
    namespace: str
    interface: dict
    ip_address: dict

    @classmethod
    def from_file(cls, path=constants.DEFAULT_CONFIG_FILE_PATH):
        with open(path, "r") as file:
            try:
                config = json.load(file)
            except JSONDecodeError as err:
                raise errors.InvalidConfigFileException(err)

        return cls.from_dict(config)

    @classmethod
    def from_dict(cls, config):
        try:
            validated = config_schema.validate(config)
        except (SchemaError, SchemaWrongKeyError) as err:
            raise errors.InvalidConfigFileException(err)

        return cls(**validated)
