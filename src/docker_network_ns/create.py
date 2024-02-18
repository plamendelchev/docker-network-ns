import logging

from pyroute2 import IPRoute, NetNS, netns

from docker_network_ns import dhcp, errors, utils

logger = logging.getLogger(__name__)


def create(config):
    # Ensure network namespace exists
    logger.debug("Creating namespace")
    try:
        netns.create(config.namespace)
    except FileExistsError as err:
        raise errors.NamespaceAlreadyExists(err)

    with IPRoute() as ip:
        # Create macvlan interface
        ip.link(
            "add",
            ifname=config.interface["name"],
            kind="macvlan",
            link=ip.link_lookup(ifname=config.interface["parent"])[0],
            macvlan_mode="private",
        )

        # Wait for interface
        macvlan_dev = ip.poll(
            ip.link, "dump", timeout=3, ifname=config.interface["name"]
        )[0]

        # Move interface to namespace
        ip.link("set", index=macvlan_dev["index"], net_ns_fd=config.namespace)

    # Enter namespace
    with NetNS(config.namespace) as ns:
        # Lookup intefaces
        lo_dev = ns.link_lookup(ifname="lo")[0]
        macvlan_dev = ns.link_lookup(ifname=config.interface["name"])[0]

        # Assign MAC address
        if config.interface["mac_address"] == "auto":
            config.interface["mac_address"] = utils.obtain_mac_from_db()

        ns.link("set", index=macvlan_dev, address=config.interface["mac_address"])

        # Set interfaces up
        ns.link("set", index=lo_dev, state="up")
        ns.link("set", index=macvlan_dev, state="up")

        # Set up IP address
        if config.ip_address["mode"] == "static":
            ns.addr("add", index=macvlan_dev, address=config.ip_address["address"])
        elif config.ip_address["mode"] == "dhcp":
            dhcp_client = dhcp.get_client(
                name=config.ip_address["dhcp_client"],
                namespace=config.namespace,
                interface=config.interface["name"],
            )
            dhcp_client.start()

    print("Success:", config)
