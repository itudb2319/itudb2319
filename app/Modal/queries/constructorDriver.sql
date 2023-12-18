SELECT d.forename, d.surname, c.name FROM drivers d
    JOIN results r ON r.driverid = d.driverid
    JOIN constructors c ON r.constructorid = c.constructorid
    JOIN races ON races.raceid = r.raceid
WHERE EXTRACT(YEAR FROM races.date) = COALESCE(%(sYear)s, EXTRACT(YEAR FROM CURRENT_DATE)) AND c.constructorid = %(sConstructorId)s
GROUP BY d.forename, d.surname, c.name
ORDER BY c.name
