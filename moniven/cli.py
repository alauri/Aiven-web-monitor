#!/bin/python3


"""Click main group and sub-commands."""


# Click imports
import click


@click.group()
def cli():
    """Main interface for Moniven."""
    click.echo(f"Hello, Moniven!")


@cli.command("produce")
def producer():
    click.echo(f"I'm the producer")


@cli.command("consume")
def consumer():
    click.echo(f"I'm the consumer")
