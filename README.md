# Website monitor

**Moniven** is a web monitor that checks a list of websites and looks for a
given pattern within the page content.

It supports multiple websites at the same time, which can be specified by
editing the file *sources.ini*.


## Requirements and configuration

This project has been tested against *Python3.9* and *Python3.10* and developed
by using [Poetry](https://python-poetry.org/) as Python package manager.

To manage the project locally you can use *Makefile*:

    $ make help


## Installation

Install production dependencies with:

    $ make install

or even the dev dependencies with:

    $ make install-dev


## Execute

Moniven is a *Command Line Interface (CLI)* developed with
[Click](https://click.palletsprojects.com/) and that exposes below commands:

 - *producer*: start a Kafka producer;
 - *consumer*: start a Kafka consumer.


## Run tests

Run tests locally with:

    $ make test

The tests suite has been developed by using [Pytest](https://docs.pytest.org/)
and supports markers. The command above runs *unit tests* only by default, but,
if you want to run all of them, use the following command:

    $ make test-all

In case you want more control over the tests suite you can activate the Poetry
shell:

    $ poetry shell

and run the command *pytest -m <test-marker>* and select one or more test
markers you want to run from the following list:

 - **unit**: run unit tests (test single functionality);
 - **sociable**: run sociable tests (test for functions interaction);
 - **acceptance**: run E2E tests (test for user interface).


### Test automation and coverage

The project supports tests automation against multiple Python versions using
[Tox](https://tox.wiki/en/latest/).

It also supports test suite coverage with a threshold of 95%.
