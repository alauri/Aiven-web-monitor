#!/bin/python3

"""Test suite for unit tests."""


# Python imports
import os

# PyTest imports
import pytest

# Project imports
from moniven.core import web


@pytest.mark.unit
def test_read(static, mocker):
    """Test the read website content routine.

    Returns:
        Nothing
    """
    target = open(os.path.join(static, "site.html"), "r").read()
    mocker.patch(
        "urllib3.PoolManager.request",
        return_value=type("A", (), {"data": target})(),
    )

    content = web.read("http://www.website.org")

    assert content == target


@pytest.mark.unit
def test_parse(static):
    """Test the HTML parser routine.

    Returns:
        Nothing
    """
    content = open(os.path.join(static, "site.html"), "r").read()
    res = web.parse(content, "main-title")

    assert res == "The main title of the page"
