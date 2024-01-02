CREATE TABLE IF NOT EXISTS drivers(
	driverId INT GENERATED ALWAYS AS IDENTITY (START WITH 860),
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
	constructorId INT GENERATED ALWAYS AS IDENTITY (START WITH 215),
	constructorRef VARCHAR(255),
	name VARCHAR(255),
	nationality VARCHAR(255),
	url VARCHAR(255),
	PRIMARY KEY(constructorId)
);

CREATE TABLE IF NOT EXISTS circuits(
	circuitId INT GENERATED ALWAYS AS IDENTITY (START WITH 80),
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
	raceId INT GENERATED ALWAYS AS IDENTITY (START WITH 1121),
	year INT,
	round INT,
	circuitId INT,
	name VARCHAR(255),
	date DATE,
	time TIME,
	url VARCHAR(255),
	fp1_date DATE,
	fp1time TIME,
	fp2date DATE,
	fp2time TIME,
	fp3date DATE,
	fp3time TIME,
	qualiDate DATE,
	qualiTime TIME,
	sprintDate DATE,
	sprintTime TIME,

	PRIMARY KEY(raceId),
	CONSTRAINT fkCircuitsRaces
		FOREIGN KEY(circuitId) REFERENCES circuits(circuitId)
		ON DELETE CASCADE
		ON UPDATE CASCADE

);

CREATE TABLE IF NOT EXISTS qualifying (
qualifyId INT GENERATED ALWAYS AS IDENTITY (START WITH 10033),
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
	FOREIGN KEY(raceId) REFERENCES races(raceId)
	ON DELETE CASCADE
	ON UPDATE CASCADE,

CONSTRAINT fkQualifyingDrivers
	FOREIGN KEY(driverId) REFERENCES drivers(driverId)
	ON DELETE CASCADE
	ON UPDATE CASCADE,

CONSTRAINT fkQualifyingConstructors
	FOREIGN KEY (constructorId)	REFERENCES constructors (constructorId)
	ON DELETE CASCADE
	ON UPDATE CASCADE

);

CREATE TABLE IF NOT EXISTS status (
	statusId INT GENERATED ALWAYS AS IDENTITY (START WITH 142),
	status VARCHAR(255),

	PRIMARY KEY(statusId)
);

CREATE TABLE IF NOT EXISTS sprintResults(
	sprintResultId INT GENERATED ALWAYS AS IDENTITY (START WITH 241),
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
		FOREIGN KEY(raceID)	REFERENCES races(raceId)
		ON DELETE CASCADE
		ON UPDATE CASCADE,

	CONSTRAINT fkDriversSprintResults
		FOREIGN KEY(driverId) REFERENCES drivers(driverId)
		ON DELETE CASCADE
		ON UPDATE CASCADE,

	CONSTRAINT fkConstructorsSprintResults
		FOREIGN KEY(constructorId) REFERENCES constructors(constructorId)
		ON DELETE CASCADE
		ON UPDATE CASCADE,

	CONSTRAINT fkStatusSprintResults
		FOREIGN KEY(statusId) REFERENCES status(statusId)
		ON DELETE CASCADE
		ON UPDATE CASCADE

);

CREATE TABLE IF NOT EXISTS results(
	resultId INT GENERATED ALWAYS AS IDENTITY (START WITH 26246),
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
		FOREIGN KEY(raceId) REFERENCES races(raceId)
		ON DELETE CASCADE
		ON UPDATE CASCADE,

	CONSTRAINT fkDriverResults
		FOREIGN KEY(driverId) REFERENCES drivers(driverId)
		ON DELETE CASCADE
		ON UPDATE CASCADE,

	CONSTRAINT fkConstructorsResults
		FOREIGN KEY(constructorId) REFERENCES constructors(constructorId)
		ON DELETE CASCADE
		ON UPDATE CASCADE,

	CONSTRAINT FkStatusResults
		FOREIGN KEY(statusId) REFERENCES status(statusId)
		ON DELETE CASCADE
		ON UPDATE CASCADE

);

CREATE TABLE IF NOT EXISTS pitStops (
	pitstopid INT GENERATED ALWAYS AS IDENTITY (START WITH 10479),
	raceId INT,
	driverId INT,
	stop INT,
	lap INT,
	time TIME,
	duration VARCHAR(255),
	milliseconds INT,

	PRIMARY KEY(pitstopid),

	CONSTRAINT fkRacesPitStops
		FOREIGN KEY(raceId) REFERENCES races(raceId)
		ON DELETE CASCADE
		ON UPDATE CASCADE,

	CONSTRAINT fkDriversPitStops
		FOREIGN KEY(driverId) REFERENCES drivers(driverId)
		ON DELETE CASCADE
		ON UPDATE CASCADE

);

CREATE TABLE IF NOT EXISTS lapTimes(
	laptimeid INT GENERATED ALWAYS AS IDENTITY (START WITH 560408),
	raceId INT,
	driverId INT,
	lap INT,
	position INT,
	time TIME,
	milliseconds INT,

	PRIMARY KEY(laptimeid),

	CONSTRAINT fkRacesLapTimes
		FOREIGN KEY(raceId) REFERENCES races(raceId)
		ON DELETE CASCADE
		ON UPDATE CASCADE,

	CONSTRAINT fkDriversLapTimes
		FOREIGN KEY(driverId) REFERENCES drivers(driverId)
		ON DELETE CASCADE
		ON UPDATE CASCADE

);

CREATE TABLE IF NOT EXISTS driverStandings (
	driverStandingsId INT GENERATED ALWAYS AS IDENTITY (START WITH 72452),
	raceId INT,
	driverId INT,
	points DECIMAL,
	position INT,
	positionText VARCHAR(255),
	wins INT,

	PRIMARY KEY (driverStandingsId),

	CONSTRAINT fkRacesDriverStandings
		FOREIGN KEY(raceId)	REFERENCES races(raceId)
		ON DELETE CASCADE
		ON UPDATE CASCADE,

	CONSTRAINT fkDriversDriverStandings
		FOREIGN KEY(driverId) REFERENCES drivers(driverId)
		ON DELETE CASCADE
		ON UPDATE CASCADE

);

CREATE TABLE IF NOT EXISTS constructorStandings(
	constructorStandingsId INT GENERATED ALWAYS AS IDENTITY (START WITH 28693),
	raceId INT,
	constructorId INT,
	points DECIMAL,
	position INT,
	positionText VARCHAR(255),
	status VARCHAR(255),

	PRIMARY KEY(constructorStandingsId),

	CONSTRAINT fkRacesConstructorStandings
		FOREIGN KEY(raceId)	REFERENCES races(raceId)
		ON DELETE CASCADE
		ON UPDATE CASCADE,

	CONSTRAINT fkConstructorsConstructorStandings
		FOREIGN KEY(constructorId) REFERENCES constructors(constructorId)
		ON DELETE CASCADE
		ON UPDATE CASCADE

);

CREATE TABLE IF NOT EXISTS constructorResults(
	constructorResultsId INT GENERATED ALWAYS AS IDENTITY (START WITH 16870),
	raceId INT,
	constructorId INT,
	points DECIMAL,
	status VARCHAR(255),

	PRIMARY KEY(constructorResultsId),

	CONSTRAINT fkRacesConstructorResults
		FOREIGN KEY(raceId) REFERENCES races(raceId)
		ON DELETE CASCADE
		ON UPDATE CASCADE,

	CONSTRAINT fkConstructorsConstructorResults
		FOREIGN KEY(constructorId) REFERENCES constructors(constructorId)
		ON DELETE CASCADE
		ON UPDATE CASCADE

);


CREATE TABLE IF NOT EXISTS quiz (
	quizId INT GENERATED ALWAYS AS IDENTITY (START WITH 2),
	questionContent VARCHAR(255),
	option1 VARCHAR(255),
	option2 VARCHAR(255),
	correctAnswer VARCHAR(255),

	PRIMARY KEY (quizId)
);

CREATE TABLE IF NOT EXISTS users(
	userId INT GENERATED ALWAYS AS IDENTITY,
	username VARCHAR(31) UNIQUE,
	profilePhoto VARCHAR(255) UNIQUE,
	blinkScore DECIMAL,
	email VARCHAR(255) UNIQUE,
	psw VARCHAR(255),
	salt VARCHAR(15),
	quizScore INT,
	userRole INT,

	PRIMARY KEY(userId),
	CONSTRAINT usernameEmailNotnull CHECK (
		NOT (
			( username IS NULL  OR  username = '' )
			AND
			( email IS NULL  OR  email = '' )
		)
	),
	CONSTRAINT usersIntegrity CHECK (
		quizScore > 0 AND
		blinkScore > 0 AND
		userRole = 0 OR userRole = 1
	)
);

CREATE TABLE IF NOT EXISTS answers(
	answerId INT GENERATED ALWAYS AS IDENTITY,
	userId INT,
	quizId INT,
	time TIMESTAMP,
	isTrue BOOLEAN,

	PRIMARY KEY (answerId),
	UNIQUE (userId, quizId, time),

	CONSTRAINT fkUserAnswers
		FOREIGN KEY(userId) REFERENCES users(userId)
		ON DELETE CASCADE
		ON UPDATE CASCADE,

	CONSTRAINT fkQuizAnswers
		FOREIGN KEY(quizId) REFERENCES quiz(quizId)
		ON DELETE CASCADE
		ON UPDATE CASCADE

);


CREATE TABLE IF NOT EXISTS lkp_tables(
	tableId INT GENERATED ALWAYS AS IDENTITY,
	tableName varchar(30),

	PRIMARY KEY (tableId)
);

INSERT INTO lkp_tables (tableName)
SELECT table_name
FROM information_schema.tables
WHERE 
	table_schema = 'public' AND table_name != 'lkp_tables';

CREATE VIEW EARLIST_WIN AS
SELECT re.driverid, 
        MIN(AGE(r.date, d.dob)) as min_age, 
        MIN(r.year) as season,
        re.positiontext
    FROM races r JOIN results re ON re.raceid = r.raceid 
    JOIN drivers d ON d.driverid = re.driverid 
    WHERE re.positiontext = '1'
    GROUP BY re.driverid, re.positiontext;

CREATE VIEW PER_WINS AS
SELECT d.forename, d.surname,
(SELECT CONCAT(MIN(r.year), ' - ', MAX(r.year))
FROM races r JOIN results re ON re.raceid = r.raceid
WHERE re.positiontext = '1' AND re.driverid = d.driverid) AS seasons,
COUNT (re.driverid) AS ENTRY, 
COUNT(CASE WHEN re.positiontext = '1' THEN 1 ELSE NULL END) AS total_wins,
ROUND((COUNT(CASE WHEN re.positiontext = '1' THEN 1 ELSE NULL END)::NUMERIC / COUNT (re.driverid))::NUMERIC * 100, 2) AS win_rate
FROM drivers d JOIN results re ON d.driverid = re.driverid 
GROUP BY d.forename, d.surname, d.driverid
ORDER BY win_rate 
DESC;

CREATE OR REPLACE FUNCTION get_race_results(slimNumber INTEGER)
RETURNS TABLE (
    forename VARCHAR(255),
    surname VARCHAR(255),
    age INTERVAL,
    name VARCHAR(255),
    season INTEGER,
    round INTEGER,
    result VARCHAR(255)
) AS $$
BEGIN
    RETURN QUERY 
    SELECT d.forename, 
    d.surname, 
    a.max_age as age, 
    r.name,
    a.season, 
    r.round, 
    re.positiontext as result 
    FROM races r JOIN results re ON re.raceid = r.raceid 
    JOIN drivers d ON d.driverid = re.driverid 
    JOIN status s ON re.statusid = s.statusid
    JOIN (SELECT re.driverid, 
            MAX(AGE(r.date, d.dob)) as max_age, 
            MIN(r.year) as season,
            s.statusid
        FROM races r JOIN results re ON re.raceid = r.raceid 
        JOIN drivers d ON d.driverid = re.driverid 
        JOIN status s ON re.statusid = s.statusid WHERE s.statusid = 1
        GROUP BY re.driverid, s.statusid
    ) a ON d.driverid = a.driverid 
    AND AGE(r.date, d.dob) = a.max_age AND s.statusid = a.statusid
    ORDER BY age DESC
    LIMIT slimNumber;
END; $$ LANGUAGE plpgsql;