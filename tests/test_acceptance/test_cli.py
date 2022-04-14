#!/bin/python3


"""Test suite entry points."""


import os

# PyTest imports
import pytest

# Click imports
from click.testing import CliRunner

# Python imports
from urllib3.exceptions import NewConnectionError

# Project imports
from moniven import cli


@pytest.mark.acceptance
def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli.cli)

    assert result.exit_code == 0
    assert "Main interface for Moniven." in result.output


@pytest.mark.acceptance
def test_produce(static, mocker):
    sources = os.path.join(static, "sources.ini")
    target = open(os.path.join(static, "site.html"), "r").read()
    mocker.patch(
        "urllib3.PoolManager.request",
        return_value=type("A", (), {"data": target})(),
    )

    runner = CliRunner()
    result = runner.invoke(cli.cli, ["produce", f"--sources={sources}"])

    assert result.exit_code == 0
    assert result.output == (
        "['The main title of the page', "
        "'The main title of the page', "
        "'The main title of the page']\n"
    )


@pytest.mark.acceptance
def test_produce_error(static, mocker):
    sources = os.path.join(static, "sources.ini")
    mocker.patch(
        "urllib3.PoolManager.request",
        side_effect=NewConnectionError(None, "Generic Error"),
    )

    runner = CliRunner()
    result = runner.invoke(cli.cli, ["produce", f"--sources={sources}"])

    assert result.exit_code == 0
    assert result.output == "[]\n"


@pytest.mark.acceptance
def test_consume():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ["consume"])

    assert result.exit_code == 0
    assert "I'm the consumer" in result.output
