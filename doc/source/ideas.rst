Ideas
=====

I have written this page to explain other ideas I haven't had during the
development but I couldn't implement in order to not run out of time.

I thought to add additional CLI commands to configure Aiven credentials to
the Kafka and Postgres instances, rather than use a lot of CLI options to
use for each command. Something like:

 - *avn-wm config kafka* with options to setup SSL certificate and remote creds;
 - *avn-wm config postgres* with options to setup remote creds.

This would avoid to use a lot of options every time you run one of the two main
commands.

Another idea to improve the readability of the code would be to organize the CLI
commands in packages and sub-packages rather than to have all of them within a
single Python module.

One additional improvement could be to check if the kafka topic already exists
and, if it doesn't, create it programmatically.
