-- Creation of metrics table
CREATE TABLE IF NOT EXISTS metrics (
	id	SERIAL	PRIMARY KEY,
	url	TEXT	NOT NULL,
	scode	INT	NOT NULL,
	texec	TEXT	NOT NULL,
	data	TEXT	NOT NULL
);
