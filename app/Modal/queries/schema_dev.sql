CREATE TABLE IF NOT EXISTS drivers(
	driverId INT GENERATED ALWAYS AS IDENTITY,
	driverRef VARCHAR(255),
	number INT,
	code VARCHAR(3),
	forename VARCHAR(255),
	surname VARCHAR(255),
	dob date,
	nationality VARCHAR(255),
	url VARCHAR(255),
	PRIMARY KEY (driverId)
);

CREATE TABLE IF NOT EXISTS constructors(
	constructorId INT GENERATED ALWAYS AS IDENTITY,
	constructorRef VARCHAR(255),
	name VARCHAR(255),
	nationality VARCHAR(255),
	url VARCHAR(255),
	PRIMARY KEY(constructorId)
);

CREATE TABLE IF NOT EXISTS circuits(
	circuitId INT GENERATED ALWAYS AS IDENTITY,
	circuitRef VARCHAR(255),
	name VARCHAR(255),
	location VARCHAR(255),
	country VARCHAR(255),
	lat DECIMAL,
	lng DECIMAL,
	alt INT,
	url VARCHAR(255),
	PRIMARY KEY(circuitId)
);

/*
	We've changed the primary key constraint, ERD was wrong in terms of logic.
	Year primary key constraint has been deleted.
*/
CREATE TABLE IF NOT EXISTS races(
	raceId INT GENERATED ALWAYS AS IDENTITY,
	year INT,
	round INT,
	circuitId INT,
	name VARCHAR(255),
	date DATE,
	time TIME,
	url VARCHAR(255),
	fp1_date DATE,
	fp1_time TIME,
	fp2_date DATE,
	fp2_time TIME,
	fp3_date DATE,
	fp3_time TIME,
	quali_date DATE,
	quali_time TIME,
	sprint_date DATE,
	sprint_time TIME,

	PRIMARY KEY(raceId),
	CONSTRAINT fkCircuitsRaces
		FOREIGN KEY(circuitId)
			REFERENCES circuits(circuitId)
);

CREATE TABLE IF NOT EXISTS qualifying (
qualifyId INT GENERATED ALWAYS AS IDENTITY,
raceId INT,
driverId INT,
constructorId INT,
number INT,
position INT,
q1 VARCHAR(255),
q2 VARCHAR(255),
q3 VARCHAR(255),
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
	statusId INT GENERATED ALWAYS AS IDENTITY,
	status VARCHAR(255),

	PRIMARY KEY(statusId)
);

CREATE TABLE IF NOT EXISTS sprintResults(
	sprintResultId INT GENERATED ALWAYS AS IDENTITY,
	raceId INT,
	driverId INT,
	constructorId INT,
	number INT,
	grid INT,
	position INT,
	positionText VARCHAR(255),
	positionOrder INT,
	points DECIMAL,
	laps INT,
	time VARCHAR(255),
	milliseconds INT,
	fastestLap INT,
	fastestLapTime VARCHAR(16),
	statusID INT,

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
	resultId INT GENERATED ALWAYS AS IDENTITY,
	raceId INT,
	driverId INT,
	constructorId INT,
	number INT,
	grid INT,
	position INT,
	positionText VARCHAR(255),
	positionOrder INT,
	points DECIMAL,
	laps INT,
	time VARCHAR(255),
	miliseconds INT,
	fastestLap INT,
	rank INT,
	fastestLapTime VARCHAR(255),
	fastestLapSpeed VARCHAR(255),
	statusId INT,

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
	raceId INT GENERATED ALWAYS AS IDENTITY,
	driverId INT GENERATED ALWAYS AS IDENTITY,
	stop INT,
	lap INT,
	time TIME,
	duration VARCHAR(255),
	milliseconds INT,

	PRIMARY KEY(raceId, driverId, stop),

	CONSTRAINT fkRacesPitStops
	FOREIGN KEY(raceId) REFERENCES races(raceId),

	CONSTRAINT fkDriversPitStops
	FOREIGN KEY(driverId) REFERENCES drivers(driverId)
);

CREATE TABLE IF NOT EXISTS lapTimes(
	raceId INT GENERATED ALWAYS AS IDENTITY,
	driverId INT GENERATED ALWAYS AS IDENTITY,
	lap INT GENERATED ALWAYS AS IDENTITY,
	position INT,
	time VARCHAR(255),
	milliseconds INT,

	PRIMARY KEY(raceId, driverId, lap),

	CONSTRAINT fkRacesLapTimes
		FOREIGN KEY(raceId) REFERENCES races(raceId),

	CONSTRAINT fkDriversLapTimes
		FOREIGN KEY(driverId) REFERENCES drivers(driverId)
);

CREATE TABLE IF NOT EXISTS driverStandings (
	driverStandingsId INT GENERATED ALWAYS AS IDENTITY,
	raceId INT,
	driverId INT,
	points DECIMAL,
	position INT,
	positionText VARCHAR(255),
	wins INT,

	PRIMARY KEY (driverStandingsId),

	CONSTRAINT fkRacesDriverStandings
		FOREIGN KEY(raceId)
			REFERENCES races(raceId),

	CONSTRAINT fkDriversDriverStandings
		FOREIGN KEY(driverId)
			REFERENCES drivers(driverId)
);

CREATE TABLE IF NOT EXISTS constructorStandings(
	constructorStandingsId INT GENERATED ALWAYS AS IDENTITY,
	raceId INT,
	constructorId INT,
	points DECIMAL,
	position INT,
	positionText VARCHAR(255),
	status VARCHAR(255),

	PRIMARY KEY(constructorStandingsId),

	CONSTRAINT fkRacesConstructorStandings
		FOREIGN KEY(raceId)
			REFERENCES races(raceId),

	CONSTRAINT fkConstructorsConstructorStandings
		FOREIGN KEY(constructorId)
			REFERENCES constructors(constructorId)
);

CREATE TABLE IF NOT EXISTS constructorResults(
	constructorResultsId INT GENERATED ALWAYS AS IDENTITY,
	raceId INT,
	constructorId INT,
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
	quizId INT GENERATED ALWAYS AS IDENTITY,
	questionContent VARCHAR(255),
	option1 VARCHAR(255),
	option2 VARCHAR(255),
	correctAnswer VARCHAR(255),

	PRIMARY KEY (quizId)
);

CREATE TABLE IF NOT EXISTS users(
	userId INT GENERATED ALWAYS AS IDENTITY,
	username VARCHAR(31),
	profilePhoto VARCHAR(255),
	blinkScore DECIMAL,
	email VARCHAR(255),
	password VARCHAR(255),
	salt VARCHAR(15),
	quizScore INT,

	PRIMARY KEY(userId)
);

CREATE TABLE IF NOT EXISTS answers(
	answerId INT,
	userId INT,
	quizId INT,
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