#!/bin/python3


"""Click main group and sub-commands."""


import configparser
import os
import time

# Python imports
from typing import Optional, Union

# Click imports
import click

# Project imports
from moniven.core import web


@click.group()
def cli():
    """Main interface for Moniven."""
    pass


@cli.command()
@click.option(
    "--sources",
    "-s",
    default=os.path.join(os.path.dirname(__file__), "..", "sources.ini"),
    help="file containing the list of URLs to parse",
)
@click.option("--loop", default=False, help="run the producer in loop")
@click.option(
    "--delay", default=60000.0, help="time to wait before the next iteration"
)
def produce(sources: str, loop: bool, delay: float):
    """Crawl a list of URLs.

    For each URL's content search for a specific target within the content of
    each.
    """
    config = configparser.ConfigParser()
    config.read(sources)

    urls = config["sources"]["urls"].replace("\n", "").split(",")
    urls = [url for url in urls if url]

    while True:
        result = []

        # For each URL to parse get its content and search for a specific tag
        # The Kafka producer will send all the data found the a remote Kafka
        # cluster
        for url in urls:
            cont: Optional[Union[str, bytes]] = web.read(url)
            if cont is None:
                continue
            cont = cont.decode("utf-8") if isinstance(cont, bytes) else cont

            # Search for data
            data = web.parse(cont, "main-title")
            if data:
                result.append(data)

        # TODO: use a Kafka producer to send data
        click.echo(result)

        # Check the loop. If true, execute the producer periodically
        if not loop:
            break
        time.sleep(delay)


@cli.command()
def consume():
    click.echo("I'm the consumer")
