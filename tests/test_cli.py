#!/bin/python3


"""Test suite entry points."""


# PyTest imports
import pytest

# Project imports
from moniven import __main__


@pytest.mark.unit
def test_entry_point():
    assert __main__.main() == "Hello, Moniven!"
