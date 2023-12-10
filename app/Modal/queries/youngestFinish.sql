SELECT d.forename, 
d.surname, 
a.min_age as age, 
r.name,
a.season, 
r.round, 
re.positiontext as result 
FROM races r JOIN results re ON re.raceid = r.raceid 
JOIN drivers d ON d.driverid = re.driverid 
JOIN status s ON re.statusid = s.statusid
JOIN (SELECT re.driverid, 
        MIN(AGE(r.date, d.dob)) as min_age, 
        MIN(r.year) as season,
        s.statusid
    FROM races r JOIN results re ON re.raceid = r.raceid 
    JOIN drivers d ON d.driverid = re.driverid 
    JOIN status s ON re.statusid = s.statusid WHERE s.statusid = 1
    GROUP BY re.driverid, s.statusid
)a ON d.driverid = a.driverid 
AND AGE(r.date, d.dob) = a.min_age AND s.statusid = a.statusid
ORDER BY age;