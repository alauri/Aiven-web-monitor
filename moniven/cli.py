#!/bin/python3


"""Click main group and sub-commands."""


# Click imports
import click


@click.group()
def cli():
    """Main interface for Moniven."""
    click.echo(f"Hello, Moniven!")


@cli.command()
def produce():
    click.echo(f"I'm the producer")


@cli.command()
def consume():
    click.echo(f"I'm the consumer")
