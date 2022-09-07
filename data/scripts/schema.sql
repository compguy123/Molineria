PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS "medication" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL UNIQUE,
	"image_url"	TEXT,
	"wiki_identifier"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "pharmacy" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL UNIQUE,
	"phone_number"	TEXT NOT NULL,
	"location"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "user" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL UNIQUE,
	"date_of_birth"	TEXT,
	"comment"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "user_medication" (
	"id"	INTEGER,
	"user_id"	INTEGER NOT NULL,
	"medication_id"	INTEGER NOT NULL,
	"rx_number"	TEXT NOT NULL UNIQUE,
	"quantity"	INTEGER NOT NULL,
	"remaining_refills"	INTEGER,
	"weight_in_milligrams"	REAL,
	"total_weight_in_milligrams"	REAL,
	"filled_on"	TEXT,
	"discard_on"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "user"("id"),
	FOREIGN KEY("medication_id") REFERENCES "medication"("id") ,
	UNIQUE ("user_id", "medication_id")
);

CREATE TABLE IF NOT EXISTS "user_medication_refill" (
	"id"	INTEGER,
	"user_medication_id"	INTEGER NOT NULL,
	"pharmacy_id"	INTEGER NOT NULL,
	"prescribed_by"	TEXT,
	"refilled_on"	TEXT,
	"amount_in_milligrams"	REAL,
	"comment"	TEXT,
	FOREIGN KEY("pharmacy_id") REFERENCES "pharmacy"("id"),
	FOREIGN KEY("user_medication_id") REFERENCES "user_medication"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "user_medication_intake" (
	"id"	INTEGER,
	"user_medication_id"	INTEGER NOT NULL,
	"time"	TEXT,
	"amount_in_milligrams"	REAL,
	"days_of_week"	TEXT,
	FOREIGN KEY("user_medication_id") REFERENCES "user_medication"("id") ON DELETE cascade ,
	PRIMARY KEY("id" AUTOINCREMENT)
);
