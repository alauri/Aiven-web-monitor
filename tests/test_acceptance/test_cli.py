#!/bin/python3


"""Test suite entry points."""


import os

# PyTest imports
import pytest

# Click imports
from click.testing import CliRunner

# Project imports
from moniven import cli


@pytest.mark.acceptance
def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli.cli)

    assert result.exit_code == 0
    assert "Main interface for Moniven." in result.output


@pytest.mark.acceptance
def test_produce(static, mocker, producer):
    # Mock urllib3
    sources = os.path.join(static, "sources.ini")
    target = open(os.path.join(static, "site.html"), "r").read()
    mocker.patch(
        "requests.get",
        return_value=type(
            "Requests",
            (),
            {"text": target, "status_code": 200, "elapsed": "0:00:00.12345"},
        ),
    )

    # Mock Kafka Producer
    mocker.patch("kafka.KafkaProducer", return_value=producer)

    runner = CliRunner()
    result = runner.invoke(cli.cli, ["produce", f"--sources={sources}"])

    assert result.exit_code == 0
    assert result.output == (
        "Data sent to topic 'topic-newpapers'\n"
        "Data sent to topic 'topic-newpapers'\n"
        "Data sent to topic 'topic-newpapers'\n"
    )


@pytest.mark.acceptance
def test_produce_error(static, mocker, producer):
    # Mock urllib3
    sources = os.path.join(static, "sources.ini")
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

    # Mock Kafka Producer
    mocker.patch("kafka.KafkaProducer", return_value=producer)

    runner = CliRunner()
    result = runner.invoke(cli.cli, ["produce", f"--sources={sources}"])

    assert result.exit_code == 0
    assert result.output == ""


@pytest.mark.acceptance
def test_consume(mocker, consumer):

    # Mock Kafka Producer
    mocker.patch("kafka.KafkaConsumer", return_value=consumer)

    runner = CliRunner()
    result = runner.invoke(cli.cli, ["consume"])

    assert result.exit_code == 0
    assert result.output == (
        "http://www.website.org:200:0:00:00.12345:The main title\n"
        "http://www.website.org:404:0:00:00.12345:Not Found\n"
    )
