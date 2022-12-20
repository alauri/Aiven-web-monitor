# Website monitor with Aiven

This project is a web monitor developed by using Aiven's services.

It checks the availability of a list of web sites specified within the file
*sources.ini* and tries to extract the data of a specific tag from their
contents; if found, the data are published to an Aiven Kafka topic by a
producer and read by a consumer that also stores them onto an Aiven Postgres
instance.

NOTE: This repo is no longer maintained and it's been archived

## Requirements and configuration

The project has been developed by using Poetry and tested against *Python3.9*
and *Python3.10*.

To manage the project locally you can use *Makefile*:

    $ make help


## Installation

Install production dependencies with:

    $ make install

or development dependencies with:

    $ make install-dev


## Build as a library

If needed, the project can also be installed as a Python library:

     $ make build
     $ pip install aiven-web-monitor-0.1.0.tar.gz


## Execute

The project exposes a *Command Line Interface (CLI)* named **avn-wm** developed
with Click with the below commands:

 - *avn-wm produce*: start the producer;
 - *avn-wm consume*: start the consumer.

Please refer to the documentation that can be built with the below command
for additional information about how to start the services or for additional
ideas about the project:

    $ make doc


## Run tests

Run tests locally with:

    $ make test

The tests suite has been developed by using Pytest and supports markers. The
command above runs *unit tests* only by default, but, if you want to run all of
them, use the following command:

    $ make test-all

In case you want more control over the tests suite you can activate the Poetry
shell:

    $ poetry shell

and run specific tests by using Pytest markers or Python module directly.
Available markers are:

 - **unit**: run unit tests (test single functionality);
 - **acceptance**: run E2E tests (test for user interface).


### Test automation and coverage

The project supports tests automation against multiple Python versions using
Tox.

It also supports test suite coverage with a threshold of 95%, just run *tox*.


## Start services

*avm-wm* can work locally for testing purposes with just the default
configuration; services can be started with Docker:

    $ make services
    $ make services-down
