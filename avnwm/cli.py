#!/bin/python3


"""Click main group and sub-commands."""


import configparser
import os
import time

import click
import kafka
import kafka.errors
import psycopg2
import psycopg2.extras

from avnwm.core import web


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
@click.option(
    "--loop/--no-loop", default=False, help="run the producer in loop"
)
@click.option(
    "--delay", default=60, help="time to wait before the next iteration"
)
@click.option(
    "--service-uri", default="localhost:9092", help="the Kafka service URI"
)
@click.option(
    "--topic",
    default="topic-papers",
    help="the Kafka topic where to send the data",
)
@click.option(
    "--ssl/--no-ssl", default=False, help="enable/disable SSL certificate"
)
@click.option("--ca", default=None, help="absolute path of file 'ca.pem'")
@click.option(
    "--cert", default=None, help="absolute path of file 'service.cert'"
)
@click.option("--key", default=None, help="absolute path of file 'service.key'")
def produce(
    sources: str,
    loop: bool,
    delay: int,
    service_uri: str,
    topic: str,
    ssl: bool,
    ca: str,
    cert: str,
    key: str,
):
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
    kwargs = {}

    if ssl:
        kwargs["security_protocol"] = "SSL"
        kwargs["ssl_cafile"] = ca
        kwargs["ssl_certfile"] = cert
        kwargs["ssl_keyfile"] = key

    producer = kafka.KafkaProducer(bootstrap_servers=[service_uri], **kwargs)

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
                try:
                    _ = producer.send(topic, data.encode("utf-8"))
                    click.echo(f"Data sent to topic '{topic}'")
                except kafka.errors.KafkaTimeoutError:
                    click.echo("Data didn't send because a timeout error")

        # Check the loop. If true, execute the producer periodically
        if not loop:
            break
        time.sleep(delay)

    # Close Producer
    producer.close()


@cli.command()
@click.option(
    "--service-uri", default="localhost:9092", help="the Kafka service URI"
)
@click.option(
    "--topic",
    default="topic-papers",
    help="the Kafka topic where to send the data",
)
@click.option(
    "--ssl/--no-ssl", default=False, help="enable/disable SSL certificate"
)
@click.option("--ca", default=None, help="absolute path of file 'ca.pem'")
@click.option(
    "--cert", default=None, help="absolute path of file 'service.cert'"
)
@click.option("--key", default=None, help="absolute path of file 'service.key'")
@click.option("--dbname", default="postgres", help="the database name")
@click.option("--dbhost", default="localhost", help="the database host")
@click.option("--dbuser", default="postgres", help="the database user")
@click.option("--dbpass", default="postgres", help="the database pass")
@click.option("--dbport", default=5438, help="the database port")
@click.option(
    "--dbschema",
    default=os.path.join(os.path.dirname(__file__), "..", "sql", "schema.sql"),
    help="the schema to initialize the database",
)
def consume(
    service_uri: str,
    topic: str,
    ssl: bool,
    ca: str,
    cert: str,
    key: str,
    dbname: str,
    dbhost: str,
    dbuser: str,
    dbpass: str,
    dbport: int,
    dbschema: str,
):
    """Consume messages from Kafka topic.

    The consumer retrieves messages from a Kafka topic and stores the
    information within a Postgres database.
    """
    # Initialize the Kafka consumer
    kwargs = {}

    if ssl:
        kwargs["security_protocol"] = "SSL"
        kwargs["ssl_cafile"] = ca
        kwargs["ssl_certfile"] = cert
        kwargs["ssl_keyfile"] = key

    consumer = kafka.KafkaConsumer(
        topic, bootstrap_servers=[service_uri], **kwargs
    )

    # Connection database initialization
    conn = psycopg2.connect(
        dbname=dbname, host=dbhost, user=dbuser, password=dbpass, port=dbport
    )

    # Get a fresh cursor
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Create table metrics onto the database
    with open(dbschema, "r") as f:
        cur.execute(f.read())
        conn.commit()

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
