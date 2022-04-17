#!/bin/python3


"""Test suite entry points."""


import os

import pytest
from click.testing import CliRunner

from avnwm import cli


@pytest.mark.acceptance
def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli.cli)

    assert result.exit_code == 0
    assert "Main interface for Moniven." in result.output


@pytest.mark.acceptance
def test_produce(static, mocker, producer):

    # Mock section
    mocker.patch("kafka.KafkaProducer", return_value=producer)
    mocker.patch("psycopg2.connect")
    mocker.patch(
        "requests.get",
        side_effect=[
            type(
                "Requests",
                (),
                {
                    "text": open(
                        os.path.join(static, "site1.html"), "r"
                    ).read(),
                    "status_code": 200,
                    "elapsed": "0:00:00.12345",
                },
            ),
            type(
                "Requests",
                (),
                {
                    "text": open(
                        os.path.join(static, "site2.html"), "r"
                    ).read(),
                    "status_code": 200,
                    "elapsed": "0:00:00.12345",
                },
            ),
            type(
                "Requests",
                (),
                {
                    "text": open(
                        os.path.join(static, "site3.html"), "r"
                    ).read(),
                    "status_code": 200,
                    "elapsed": "0:00:00.12345",
                },
            ),
        ],
    )

    runner = CliRunner()
    result = runner.invoke(
        cli.cli,
        [
            "produce",
            "--ssl",
            f"--ca={os.path.join(static, 'ca.pem')}",
            f"--cert={os.path.join(static, 'service.cert')}",
            f"--key={os.path.join(static, 'service.key')}",
            f"--sources={os.path.join(static, 'sources.ini')}",
        ],
    )

    assert result.exit_code == 0
    assert result.output == (
        "Data sent to topic 'topic-papers'\n"
        "Data sent to topic 'topic-papers'\n"
        "Data sent to topic 'topic-papers'\n"
    )


@pytest.mark.acceptance
def test_produce_error(static, mocker, producer):

    # Mock section
    mocker.patch("kafka.KafkaProducer", return_value=producer)
    mocker.patch("psycopg2.connect")
    mocker.patch(
        "requests.get",
        return_value=type(
            "Requests",
            (),
            {
                "reason": "Not Found",
                "status_code": 404,
                "elapsed": "0:00:00.12345",
            },
        ),
    )

    sources = os.path.join(static, "sources.ini")
    runner = CliRunner()
    result = runner.invoke(cli.cli, ["produce", f"--sources={sources}"])

    assert result.exit_code == 0
    assert result.output == ""


@pytest.mark.acceptance
def test_consume(mocker, static, consumer):

    # Mock section
    mocker.patch("kafka.KafkaConsumer", return_value=consumer)
    mocker.patch("psycopg2.connect")

    runner = CliRunner()
    result = runner.invoke(
        cli.cli,
        [
            "consume",
            "--ssl",
            f"--ca={os.path.join(static, 'ca.pem')}",
            f"--cert={os.path.join(static, 'service.cert')}",
            f"--key={os.path.join(static, 'service.key')}",
            "--dbname=testdb",
            "--dbhost=localhost",
            "--dbuser=test",
            "--dbpass=test",
            "--dbport=12345",
            f"--dbschema={os.path.join(static, 'schema.sql')}",
        ],
    )

    assert result.exit_code == 0
    assert result.output == "Stored data: Main title\nStored data: Not Found\n"
