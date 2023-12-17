SELECT d.forename, d.surname, CONCAT(MIN(r.year), '-', MAX(r.year)) AS seasons, d.dob, d.nationality, d.number 
FROM drivers d 
JOIN results re ON re.driverid = d.driverid 
JOIN races r ON re.raceid = r.raceid
WHERE d.forename = %(sDriverName)s AND d.surname = %(sDriverSurname)s 
GROUP BY d.forename, d.surname, d.dob, d.nationality, d.number;


