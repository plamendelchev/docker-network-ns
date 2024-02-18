import logging

from pyroute2 import IPRoute, netns

from docker_network_ns import dhcp, errors

logger = logging.getLogger(__name__)


def remove(config):
    logger.debug("Start removing setup")

    ns = netns.listnetns()
    logger.debug(f"Namespaces found: {ns}")

    if config.namespace not in ns:
        logger.debug(f"{config.namespace} not found")
    else:
        logger.debug(f"{config.namespace} found")

        if config.ip_address["mode"] == "dhcp":
            dhcp_client = dhcp.get_client(
                name=config.ip_address["dhcp_client"],
                namespace=config.namespace,
                interface=config.interface["name"],
            )
            dhcp_client.stop()

        logger.debug(f"Removing namespace {config.namespace}")
        try:
            netns.remove(config.namespace)
        except OSError as err:
            raise errors.UnableToDeleteNamespace(err)
        logger.debug("Namespace removed successfully")

    with IPRoute() as ipr:
        # Remove maclan interface from default NS
        if macvlan_dev := ipr.link_lookup(ifname=config.interface["name"]):
            logger.debug(
                f"Removing inteface {config.interface['name']} from default namespace"
            )
            ipr.link("del", index=macvlan_dev[0])

    print("Success")
