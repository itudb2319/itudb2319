SELECT d.forename, d.surname, c.name
FROM drivers d
JOIN results re ON re.driverid = d.driverid
JOIN constructors c ON re.constructorid = c.constructorid
JOIN races r ON r.raceid = re.raceid
WHERE r.year = COALESCE(%(sYear)s, (SELECT MAX(r.year) FROM races r))
      AND c.constructorid = %(sConstructorId)s
GROUP BY d.forename, d.surname, c.name
ORDER BY c.name;
