#!/bin/python3

"""Test suite configuration."""


# Python imports
import os

# PyTest imports
import pytest


@pytest.fixture(scope="session")
def static() -> str:
    """Get the absolute path of the static folder.

    Returns:
        The absolute path of the static folder.
    """
    fld = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    return fld


@pytest.fixture(autouse=True)
def wrap_every_test() -> None:
    """Wrap every single test with action that must be occur before and after.

    Returns:
        Nothing
    """
    # Setup: fill with any logic you want

    yield

    # Teardown : fill with any logic you want
