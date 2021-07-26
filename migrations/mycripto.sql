CREATE TABLE "movimientos" (
	"id"	INTEGER,
	"fecha"	TEXT,
	"hora"	TEXT,
	"moneda_from"	TEXT,
	"cantidad_from"	REAL,
	"moneda_to"	TEXT,
	"cantidad_to"	REAL,
	"pu"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
)