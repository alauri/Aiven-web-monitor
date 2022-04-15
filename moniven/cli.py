#!/bin/python3


"""Click main group and sub-commands."""


import configparser
import os
import time

# Click imports
import click

# Kafka imports
import kafka
import psycopg2

# Psycopg2 imports
import psycopg2.extras

# Project imports
from moniven.core import web


@click.group()
def cli():
    """Main interface for Moniven."""
    pass


@cli.command()
@click.option(
    "--sources",
    default=os.path.join(os.path.dirname(__file__), "..", "sources.ini"),
    help="file containing the list of URLs to parse",
)
@click.option("--loop", default=False, help="run the producer in loop")
@click.option(
    "--delay", default=60000.0, help="time to wait before the next iteration"
)
@click.option("--server", default="localhost:9092", help="the Kafka server")
@click.option(
    "--topic",
    default="topic-newpapers",
    help="the Kafka topic where to send the data",
)
def produce(sources: str, loop: bool, delay: float, server: str, topic: str):
    """Crawl a list of URLs.

    For each URL's content search for a specific target within the content of
    each.
    """
    # Get the list of URLs to crawl from the configuration file
    config = configparser.ConfigParser()
    config.read(sources)

    urls = config["sources"]["urls"].replace("\n", "").split(",")
    urls = [url for url in urls if url]

    # Initialize the producer
    producer = kafka.KafkaProducer(bootstrap_servers=[server])

    while True:
        # For each URL to parse get its content and search for a specific tag
        # The Kafka producer will send all the data found the a remote Kafka
        # cluster
        for url in urls:
            cont, info = web.read(url)

            # Search for data and send it to Kafka
            data = web.parse(cont, "main-title")
            if data:
                data = f"{info},{data}"
                _ = producer.send(topic, data.encode("utf-8"))
                click.echo(f"Data sent to topic '{topic}'")

        # Check the loop. If true, execute the producer periodically
        if not loop:
            break
        time.sleep(delay)

    # Close Producer
    producer.close()


@cli.command()
@click.option("--loop", default=False, help="run the producer in loop")
@click.option(
    "--delay", default=60000.0, help="time to wait before the next iteration"
)
@click.option("--server", default="localhost:9092", help="the Kafka server")
@click.option(
    "--topic",
    default="topic-newpapers",
    help="the Kafka topic where to send the data",
)
def consume(loop: bool, delay: float, server: str, topic: str):
    """Crawl a list of URLs.

    For each URL's content search for a specific target within the content of
    each.
    """
    # Initialize the Kafka consumer
    consumer = kafka.KafkaConsumer(topics=topic, bootstrap_servers=[server])

    # Connection database initialization
    conn = psycopg2.connect(
        dbname="testdb",
        host="localhost",
        user="testuser",
        passwork="testpwd",
        port=5432,
    )

    while True:
        # Get a fresh cursor
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Iter over all new messages
        for message in consumer:
            # Execute a query
            url, scode, texec, data = message.value.split(",")
            cur.execute(
                "INSERT INTO metrics VALUES(%s, %s, %s, %s)",
                (url, scode, texec, data),
            )
            click.echo(f"Stored data: {data}")

        # Commit records
        conn.commit()
        click.echo("All records have been saved")

        # Check the loop. If true, execute the producer periodically
        if not loop:
            break
        time.sleep(delay)

    # Close Consumer
    consumer.close()
