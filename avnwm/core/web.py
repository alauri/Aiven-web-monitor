#!/bin/python3


"""Utility for HTML pages."""


from html.parser import HTMLParser
from typing import Tuple

import requests


class WebsiteParser(HTMLParser):
    def __init__(self, target, *args, **kwargs):
        self._target = target
        self._found = False
        self._read = False
        self._data = ""

        super().__init__(*args, **kwargs)

    def handle_starttag(self, _, attrs) -> None:
        """Search of the target within the page content, if found, read the
        related data information.

        Args:
            _: the tag;
            attrs: the list of the attributes.

        Returns:
            Nothing
        """
        # Search over all the attributes to find the target.
        for attr in attrs:
            if attr[1] == self._target:
                self._read = True
                return

    def handle_data(self, data) -> None:
        """Read the tag data if the target has been found.

        Args:
            data: the current tag's data information.

        Returns:
            Nothing
        """
        # Read only the first occurrence of a specific target attribute
        if not self._found and self._read:
            self.data = data
            self._found = True

    @property
    def data(self) -> str:
        """The data of the found target.

        Returns:
            The data as a string
        """
        return self._data

    @data.setter
    def data(self, new) -> None:
        """Set the new value for data.

        Returns:
            Nothing
        """
        self._data = new


def read(url: str) -> Tuple[str, str]:
    """Retrieve the website content.

    Args:
        url: the URL to read.

    Returns:
        The website's content page.
    """
    success = 200

    resp = requests.get(url)
    info = f"{url},{resp.status_code},{resp.elapsed}"
    if resp.status_code != success:
        content = resp.reason
    else:
        content = resp.text.replace(",", "")
    return content, info


def parse(content: str, target: str) -> str:
    """Parse a HTML content and extract information about a given target.

    The target the label of a specific attribute within the content. If multiple
    attributes have the same value, only the first occurrence is returned.

    Args:
        content: the HTML content;
        target: the value of the HTML tag to search for.

    Returns:
        The first occurrence of a target.
    """
    parser = WebsiteParser(target)
    parser.feed(content)
    return parser.data
