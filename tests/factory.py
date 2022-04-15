#!/bin/python3

"""Factory objects for tests."""


class Messages:
    """A predefined object to emulate messages read by a Kafka Consumer mock."""

    def __init__(self):
        self._messages = [
            type(
                "Message",
                (),
                {"value": b"http://www.website.org,200,0:00:00.123,Main title"},
            ),
            type(
                "Message",
                (),
                {"value": b"http://www.website.org,404,0:00:00.123,Not Found"},
            ),
        ]
        self._curr = 0

    def __next__(self):
        if self._curr < len(self._messages):
            data = self._messages[self._curr]
            self._curr += 1
            return data
        raise StopIteration


class Consumer:
    """A Kafka Consumer mock."""

    def __iter__(self) -> Messages:
        return Messages()

    def close(self) -> bool:
        return True


class Producer:
    """A Kafka Producer mock."""

    def send(self, *args) -> bool:
        return True

    def close(self) -> bool:
        return True
