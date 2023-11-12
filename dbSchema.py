query=\
"""
CREATE TABLE IF NOT EXISTS drivers(
	driverId SERIAL,
	driverRef varchar(255),
	number integer,
	code varchar(3),
	forename varchar(255),
	surname varchar(255),
	dob date,
	nationality varchar(255),
	url varchar(255),
	PRIMARY KEY (driverId)
);

CREATE TABLE IF NOT EXISTS constructors(
	constructorId SERIAL,
	constructorRef VARCHAR(255),
	name VARCHAR(255),
	nationality VARCHAR(255),
	url VARCHAR(255),
	PRIMARY KEY(constructorId)
);

CREATE TABLE IF NOT EXISTS circuits(
	circuitId SERIAL,
	circuitRef VARCHAR(255),
	name VARCHAR(255),
	location VARCHAR(255),
	country VARCHAR(255),
	lat DECIMAL,
	lng DECIMAL,
	alt INTEGER,
	url VARCHAR(255),
	PRIMARY KEY(circuitId)
);

CREATE TABLE IF NOT EXISTS races(
	raceId SERIAL,
	year INTEGER,
	round INTEGER,
	circuitId INTEGER,
	name VARCHAR(255),
	date DATE,
	time VARCHAR(30),
	url VARCHAR(255),
	fp1_date DATE,
	fp1_time VARCHAR(255),
	fp2_date DATE,
	fp2_time VARCHAR(255),
	fp3_date DATE,
	fp3_time VARCHAR(255),
	quali_date DATE,
	quali_time VARCHAR(255),
	sprint_date DATE,
	sprint_time VARCHAR(255),

	PRIMARY KEY(raceId),
	CONSTRAINT fkCircuitsRaces
		FOREIGN KEY(circuitId)
			REFERENCES circuits(circuitId)
);

CREATE TABLE IF NOT EXISTS qualifying (
qualifyId SERIAL,
raceId integer,
driverId integer,
constructorId integer,
number integer,
position integer,
q1 varchar(255),
q2 varchar(255),
q3 varchar(255),
PRIMARY KEY (qualifyId),
CONSTRAINT fkQualifyingRaces
	FOREIGN KEY(raceId)
		REFERENCES races(raceId),
CONSTRAINT fkQualifyingDrivers
	FOREIGN KEY(driverId)
		REFERENCES drivers(driverId),
CONSTRAINT fkQualifyingConstructors
	FOREIGN KEY (constructorId)
		REFERENCES constructors (constructorId)
);

CREATE TABLE IF NOT EXISTS status (
	statusId SERIAL,
	status VARCHAR(255),

	PRIMARY KEY(statusId)
);

CREATE TABLE IF NOT EXISTS sprintResults(
	sprintResultId SERIAL,
	raceId INTEGER,
	driverId INTEGER,
	constructorId INTEGER,
	number INTEGER,
	grid INTEGER,
	position INTEGER,
	positionText VARCHAR(255),
	positionOrder INTEGER,
	points DECIMAL,
	laps INTEGER,
	time VARCHAR(255),
	milliseconds INTEGER,
	fastestLap INTEGER,
	fastestLapTime VARCHAR(16),
	statusID integer,

	PRIMARY KEY(sprintResultId),
	CONSTRAINT fkRacesSprintResults
		FOREIGN KEY(raceID)
			REFERENCES races(raceId),

	CONSTRAINT fkDriversSprintResults
		FOREIGN KEY(driverId)
			REFERENCES drivers(driverId),

	CONSTRAINT fkConstructorsSprintResults
		FOREIGN KEY(constructorId)
			REFERENCES constructors(constructorId),

	CONSTRAINT fkStatusSprintResults
		FOREIGN KEY(statusId)
			REFERENCES status(statusId)
);

CREATE TABLE IF NOT EXISTS results(
	resultId SERIAL,
	raceId INTEGER,
	driverId INTEGER,
	constructorId INTEGER,
	number INTEGER,
	grid INTEGER,
	position INTEGER,
	positionText VARCHAR(255),
	positionOrder INTEGER,
	points DECIMAL,
	laps INTEGER,
	time VARCHAR(255),
	miliseconds INTEGER,
	fastestLap INTEGER,
	rank INTEGER,
	fastestLapTime VARCHAR(255),
	fastestLapSpeed VARCHAR(255),
	statusId INTEGER,

	PRIMARY KEY(resultId),

	CONSTRAINT fkRacesResults
		FOREIGN KEY(raceId)
			REFERENCES races(raceId),

	CONSTRAINT fkDriverResults
		FOREIGN KEY(driverId)
			REFERENCES drivers(driverId),

	CONSTRAINT fkConstructorsResults
		FOREIGN KEY(constructorId)
			REFERENCES constructors(constructorId),

	CONSTRAINT FkStatusResults
		FOREIGN KEY(statusId)
			REFERENCES status(statusId)
);

CREATE TABLE IF NOT EXISTS pitStops (
	raceId SERIAL,
	driverId SERIAL,
	stop INTEGER,
	lap INTEGER,
	time VARCHAR(255),
	duration VARCHAR(255),
	milliseconds INTEGER,

	PRIMARY KEY(raceId, driverId, stop),

	CONSTRAINT fkRacesPitStops
	FOREIGN KEY(raceId) REFERENCES races(raceId),

	CONSTRAINT fkDriversPitStops
	FOREIGN KEY(driverId) REFERENCES drivers(driverId)
);

CREATE TABLE IF NOT EXISTS lapTimes(
	raceId SERIAL,
	driverId SERIAL,
	lap SERIAL,
	position INTEGER,
	time VARCHAR(255),
	milliseconds INTEGER,

	PRIMARY KEY(raceId, driverId, lap),

	CONSTRAINT fkRacesLapTimes
		FOREIGN KEY(raceId) REFERENCES races(raceId),

	CONSTRAINT fkDriversLapTimes
		FOREIGN KEY(driverId) REFERENCES drivers(driverId)
);

CREATE TABLE IF NOT EXISTS driverStandings (
	driverStandingsId SERIAL,
	raceId integer,
	driverId integer,
	points decimal,
	position integer,
	positionText varchar(255),
	wins integer,

	PRIMARY KEY (driverStandingsId),

	CONSTRAINT fkRacesDriverStandings
		FOREIGN KEY(raceId)
			REFERENCES races(raceId),

	CONSTRAINT fkDriversDriverStandings
		FOREIGN KEY(driverId)
			REFERENCES drivers(driverId)
);

CREATE TABLE IF NOT EXISTS constructorStandings(
	constructorStandingsId SERIAL,
	raceId INTEGER,
	constructorId INTEGER,
	points DECIMAL,
	position INTEGER,
    positionText VARCHAR(255),
    wins INTEGER,

	PRIMARY KEY(constructorStandingsId),

	CONSTRAINT fkRacesConstructorStandings
		FOREIGN KEY(raceId)
			REFERENCES races(raceId),

	CONSTRAINT fkConstructorsConstructorStandings
		FOREIGN KEY(constructorId)
			REFERENCES constructors(constructorId)
);

CREATE TABLE IF NOT EXISTS constructorResults(
	constructorResultsId SERIAL,
	raceId INTEGER,
	constructorId INTEGER,
	points DECIMAL,
	status VARCHAR(255),

	PRIMARY KEY(constructorResultsId),

	CONSTRAINT fkRacesConstructorResults
		FOREIGN KEY(raceId)
			REFERENCES races(raceId),

	CONSTRAINT fkConstructorsConstructorResults
		FOREIGN KEY(constructorId)
			REFERENCES constructors(constructorId)
);


CREATE TABLE IF NOT EXISTS quiz (
	quizId SERIAL,
	questionContent varchar(255),
	option1 varchar(255),
	option2 varchar(255),
	correctAnswer varchar(255),

	PRIMARY KEY (quizId)
);

CREATE TABLE IF NOT EXISTS users(
	userId SERIAL,
	username VARCHAR(31),
	profilePhoto VARCHAR(255),
	blinkScore DECIMAL,
	email VARCHAR(255),
	password VARCHAR(255),
	salt VARCHAR(15),
	quizScore INTEGER,

	PRIMARY KEY(userId)
);

CREATE TABLE IF NOT EXISTS answers(
    answerId INTEGER,
	userId INTEGER,
	quizId INTEGER,
	time TIMESTAMP,
	isTrue BOOLEAN,

    PRIMARY KEY (answerId),
	UNIQUE (userId, quizId, time),

	CONSTRAINT fkUserAnswers
		FOREIGN KEY(userId)
			REFERENCES users(userId),

	CONSTRAINT fkQuizAnswers
		FOREIGN KEY(quizId)
			REFERENCES quiz(quizId)
);
"""

import psycopg2
import os

try:
    DATABASE_URL="postgresql://itudb2319:IqZBVpdW9dyX2LR1865w7g@onlyf1ns-11462.8nj.cockroachlabs.cloud:26257/f1?sslmode=verify-full"
    conn = psycopg2.connect(DATABASE_URL)
except psycopg2.Error as e:
    print("Connection Error!")

else: 
    with conn.cursor() as cursor:
        try:
            cursor.execute(query)
            conn.commit()
        except psycopg2.Error as e:
            print(e)