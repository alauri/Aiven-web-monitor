``avnwm.cli`` - The command line interface
==========================================

The *avn-wm* is a command line interface that exposes two commands:

 - **produce**: to check and produce data from a list of URLs to crawl through
                an Aiven Kafka topic;
 - **consume**: a Kafka consumer to get data from the topic and store them onto
                an Aiven Postgres database.

The list of URLs to crawl is defined within the file *sources.ini* with a list
labels a section for each of them where are specified the website's URL and the
tag to search for.

To add an URL to the list, just define a label to append under the section
*sources* and key *labels*, plus a new section for the new label with the
keys *url* and *target*.

For each url the monitor tries to retrieve the data from the target and, if
found, sends it to the Kafka topic **topic-papers** by default.

On the other hand, the consumer is attached to the same topic and consumes
each message and stores all the information onto an Aiven Postgres database.


The Producer
------------

The procuder can be executed one time or in loop by using the option *--loop*
and *--delay* with the elapsed time in seconds.

::

    $ avn-wm produce

or

::

    $ avn-wm produce --loop --delay 60


Check out the other flags with:

::

    $ avn-wm produce --help


Without flags this command tries to connect to a local Kafka service that can be
started with Docker.


The Consumer
------------

It automatically subscribes to the topic and waits for messages.

To connect the consumer to an Aiven Postgres instance you have to specify the
database info:

::

    $ avn-wm consume --dbname <name> --dbhost <host> --dbuser <user> --dbpass <pass> --dbport <port>


Check out the other flags with:

::

    $ avn-wm consume --help


Without flags this command tries to connect to a local Kafka service that can be
started with Docker.


The local services
------------------

To run above commands locally you have to start local Kafka and Postgres
services with:

::

    $ make services


The SSL certificate
-------------------

Both commands supports the SSL certificate for the Aiven Kafka instance and
that can be enabled with the flag *--ssl* and a set of other flag to specify
the ssl certificate files:

::

    $ avn-wm <command> --server <the-server-uri> --ssl --ca ca.pem --cert service.cert --key service.key
