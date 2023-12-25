WITH lastRace AS (
    SELECT raceid FROM races
    WHERE round = (SELECT max(round) FROM races WHERE year = %(yr)s) AND
    year = %(yr)s
    )
SELECT ds.position, d.surname || ', ' || d.forename, d.nationality, ds.points, ds.wins
 FROM driverstandings AS ds
    JOIN lastRace USING (raceid)
    JOIN drivers AS d USING (driverid)
    ORDER BY position;