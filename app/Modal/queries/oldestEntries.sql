SELECT d.forename, 
d.surname, 
a.max_age as age, 
r.name,
a.season, 
r.round, 
s.status as result 
FROM races r JOIN results re ON re.raceid = r.raceid 
JOIN drivers d ON d.driverid = re.driverid 
JOIN status s ON re.statusid = s.statusid
JOIN (SELECT re.driverid, 
        MAX(AGE(r.date, d.dob)) as max_age, 
        MIN(r.year) as season 
    FROM races r JOIN results re ON re.raceid = r.raceid 
    JOIN drivers d ON d.driverid = re.driverid 
    GROUP BY re.driverid
)a ON d.driverid = a.driverid 
AND AGE(r.date, d.dob) = a.max_age
ORDER BY age DESC;