Ideas
=====

I have written this page to explain other ideas I haven't had the time to
implement in order to not run out of time.

I thought to add additional CLI commands to configure Aiven credentials to
the Kafka and Postgres instances, rather than use a lot of CLI options to
use for each command. Something like:

 - *avn-wm config kafka* with the right flags;
 - *avn-wm config postgres* with the right flags.

With these all the other flags for the other commands can be removed or used
in different ways.
