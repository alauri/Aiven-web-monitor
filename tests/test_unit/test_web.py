#!/bin/python3

"""Test suite for unit tests."""


# Python imports
import os

# Project imports
from moniven.core import web


def test_read(static, mocker):
    """Test the read website content routine.

    Returns:
        Nothing
    """
    target = open(os.path.join(static, 'site1.html'), 'r').read()
    mocker.patch('urllib3.PoolManager.request',
                 return_value=type("A", (), {"data": target})())

    content = web.read('http://www.website1.org')

    assert content == target


def test_parse(static):
    """Test the HTML parser routine.

    Returns:
        Nothing
    """
    content = open(os.path.join(static, 'site1.html'), 'r').read()
    res = web.parse(content, "main-title")    

    assert res == "The main title of the page"
