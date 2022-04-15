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
    default="topic-papers",
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

    # Get the list of urls and the related target to search for within the
    # content
    labels = config["sources"]["labels"].replace("\n", "").split(",")
    labels = [label for label in labels if label]

    # Initialize the producer
    producer = kafka.KafkaProducer(bootstrap_servers=[server])

    while True:
        # For each URL to parse get its content and search for a specific tag
        # The Kafka producer will send all the data found the a remote Kafka
        # cluster
        for label in labels:
            cont, info = web.read(config[label]["url"])

            # Search for data and send it to Kafka
            data = web.parse(cont, config[label]["target"])
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
@click.option("--server", default="localhost:9092", help="the Kafka server")
@click.option(
    "--topic",
    default="topic-papers",
    help="the Kafka topic where to send the data",
)
@click.option("--dbhost", default="localhost", help="the database host")
@click.option("--dbuser", default="postgres", help="the database user")
@click.option("--dbpass", default="postgres", help="the database pass")
@click.option("--dbport", default=5438, help="the database port")
def consume(
    server: str,
    topic: str,
    dbhost: str,
    dbuser: str,
    dbpass: str,
    dbport: int,
):
    """Consume messages from Kafka topic.

    The consumer retrieves messages from a Kafka topic and stores the
    information within a Postgres database.
    """
    # Initialize the Kafka consumer
    consumer = kafka.KafkaConsumer(topic, bootstrap_servers=[server])

    # Connection database initialization
    conn = psycopg2.connect(
        host=dbhost, user=dbuser, password=dbpass, port=dbport
    )

    # Get a fresh cursor
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        # Iter over all new messages
        for message in consumer:
            # Execute a query
            url, scode, texec, data = message.value.decode("utf-8").split(",")
            cur.execute(
                "INSERT INTO metrics (url, scode, texec, data) VALUES (%s, %s, %s, %s)",  # noqa: E501
                (url, scode, texec, data),
            )
            conn.commit()
            click.echo(f"Stored data: {data}")
    except KeyboardInterrupt:
        click.echo("Consumer interrupted")

    # Close Consumer
    consumer.close()
