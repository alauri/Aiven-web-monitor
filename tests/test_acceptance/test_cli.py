#!/bin/python3


"""Test suite entry points."""


# Click imports
from click.testing import CliRunner

# PyTest imports
import pytest

# Project imports
from moniven import (
    __main__,
    cli
)


@pytest.mark.acceptance
def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli.cli)

    assert result.exit_code == 0
    assert 'Main interface for Moniven.' in result.output


@pytest.mark.acceptance
def test_producer():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ["produce"])

    assert result.exit_code == 0
    assert 'Hello, Moniven!' in result.output
    assert 'I\'m the producer' in result.output


@pytest.mark.acceptance
def test_consumer():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ["consume"])

    assert result.exit_code == 0
    assert 'Hello, Moniven!' in result.output
    assert 'I\'m the consumer' in result.output
