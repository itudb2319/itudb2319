SELECT d.forename, d.surname, d.nationality, COALESCE(d.number, -1), c.name || ', ' || c.country, r.year, CONCAT(COALESCE(res.fastestlap, 0), '/', res.laps), res.position, regexp_replace(res.positiontext, '[^a-zA-Z]', '', 'g'),
      d.driverid, c.circuitid, r.raceid
FROM drivers AS d
JOIN results AS res USING(driverid)
JOIN races AS r ON r.raceid = res.raceid AND
      (r.year = %(raceYear)s OR %(raceYear)s IS NULL)
JOIN circuits AS c ON c.circuitid = r.circuitid AND
      (LOWER(c.circuitRef) LIKE %(circuitRef)s OR LOWER(c.name) LIKE %(circuitRef)s OR LOWER(c.country) LIKE %(circuitRef)s OR LOWER(c.location) LIKE %(circuitRef)s)
ORDER BY (res.position, d.surname)
LIMIT %(respNumber)s;