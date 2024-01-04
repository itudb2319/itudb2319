SELECT d.forename, d.surname, CONCAT(MIN(r.year), '-', MAX(r.year)) AS seasons, d.dob, d.nationality, COALESCE(d.number, -1) 
FROM drivers d 
JOIN results re ON re.driverid = d.driverid 
JOIN races r ON re.raceid = r.raceid
WHERE d.driverid = %(sDriverId)s
GROUP BY d.forename, d.surname, d.dob, d.nationality, d.number;