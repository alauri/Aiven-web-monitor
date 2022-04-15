#!/bin/python3

"""Test suite for unit tests."""


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
    target = open(os.path.join(static, "site1.html"), "r").read()
    mocker.patch(
        "requests.get",
        return_value=type(
            "Requests",
            (),
            {"text": target, "status_code": 200, "elapsed": "0:00:00.12345"},
        ),
    )
    content, info = web.read("http://www.website1.org")

    assert (
        f"{info},{content}"
        == f"http://www.website1.org,200,0:00:00.12345,{target}"
    )


@pytest.mark.unit
def test_read_error(mocker):
    """Test the read routine when an error occur.

    Returns:
        Nothing
    """
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
    content, info = web.read("http://www.website1.org")

    assert (
        f"{info},{content}"
        == "http://www.website1.org,404,0:00:00.12345,Not Found"
    )


@pytest.mark.unit
def test_parse(static):
    """Test the HTML parser routine.

    Returns:
        Nothing
    """
    content = open(os.path.join(static, "site1.html"), "r").read()
    res = web.parse(content, "main-title1")

    assert res == "The main title of the page"
