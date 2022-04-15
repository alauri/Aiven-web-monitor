#!/bin/python3

"""Test suite configuration."""


import os

# PyTest imports
import pytest

# Project imports
from tests import factory


@pytest.fixture(scope="session")
def static() -> str:
    """Get the absolute path of the static folder.

    Returns:
        The absolute path of the static folder.
    """
    fld = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
    return fld


@pytest.fixture(scope="module")
def producer() -> factory.Producer:
    """Emulate a Kafka Producer as a mock for testing purposes.

    Returns:
        A Producer instance.
    """
    return factory.Producer()


@pytest.fixture(scope="module")
def consumer() -> factory.Consumer:
    """Emulate a Kafka Consumer as a mock for testing purposes.

    Returns:
        A Consumer instance.
    """
    return factory.Consumer()


@pytest.fixture(autouse=True)
def wrap_every_test():
    """Wrap every single test with action that must be occur before and after.

    Returns:
        Nothing
    """
    # Setup: fill with any logic you want

    yield

    # Teardown : fill with any logic you want
