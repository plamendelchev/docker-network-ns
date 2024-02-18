import logging

import click

import docker_network_ns
from docker_network_ns.constants import DEFAULT_CONFIG_FILE_PATH


@click.group()
@click.option("-d", "--debug", is_flag=True, show_default=True, default=False)
@click.option(
    "-c",
    "--config",
    "config_file",
    default=DEFAULT_CONFIG_FILE_PATH,
    show_default=True,
    type=click.Path(exists=True, dir_okay=False),
)
@click.pass_context
def cli(context, config_file, debug):
    context.obj = docker_network_ns.Config.from_file(path=config_file)

    level = logging.DEBUG if debug else logging.WARNING
    logging.basicConfig(format="%(levelname)s: %(message)s", level=level)


@cli.command()
@click.pass_obj
def create(config):
    docker_network_ns.create(config)


@cli.command()
@click.pass_obj
def remove(config):
    docker_network_ns.remove(config)


@cli.command()
@click.pass_obj
def check_config(config):
    print(config)
