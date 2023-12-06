WITH lastRace AS (
    SELECT * FROM races
    /*WHERE date = (SELECT MAX(date) FROM races)*/
    WHERE raceid = 1118/* because last race details are not present */
)

SELECT c.name || ', ' || c.location || ', ' || c.country, l.time, l.lap, d.forename || ' ' || d.surname AS name, d.nationality
FROM
    (
        SELECT driverid, MIN(milliseconds) AS bestLap
        FROM laptimes
        WHERE raceid = (SELECT raceid FROM lastRace)
        GROUP BY driverid
    ) AS bestLaps
JOIN laptimes AS l
    ON l.driverid = bestLaps.driverid AND
    l.milliseconds = bestLaps.bestLap
JOIN drivers AS d
    ON l.driverid = d.driverid
JOIN circuits AS c
    ON c.circuitid = (SELECT circuitid FROM lastRace)
ORDER BY bestLaps.bestLap;