SELECT d.forename, d.surname, d.nationality, d.number, c.name || ', ' || c.country, r.year, CONCAT(res.fastestlap, '/', res.laps), res.position, regexp_replace(res.positiontext, '[^a-zA-Z]', '', 'g')
FROM drivers AS d
JOIN results AS res USING(driverid)
JOIN races AS r ON r.raceid = res.raceid AND
      (r.year = %(raceYear)s OR %(raceYear)s IS NULL)
JOIN circuits AS c ON c.circuitid = r.circuitid AND
      (LOWER(c.circuitRef) LIKE %(circuitRef)s OR LOWER(c.name) LIKE %(circuitRef)s OR LOWER(c.country) LIKE %(circuitRef)s OR LOWER(c.location) LIKE %(circuitRef)s)
ORDER BY (res.position, d.surname)
LIMIT %(respNumber)s;