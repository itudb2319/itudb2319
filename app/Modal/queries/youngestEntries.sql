SELECT d.forename, 
d.surname, 
a.min_age as age,
r.name, 
a.season, 
r.round, 
s.status as result 
FROM races r JOIN results re ON re.raceid = r.raceid 
JOIN drivers d ON d.driverid = re.driverid 
JOIN status s ON re.statusid = s.statusid
JOIN (SELECT re.driverid, 
        MIN(AGE(r.date, d.dob)) as min_age, 
        MIN(r.year) as season 
    FROM races r JOIN results re ON re.raceid = r.raceid 
    JOIN drivers d ON d.driverid = re.driverid 
    GROUP BY re.driverid
)a ON d.driverid = a.driverid 
AND AGE(r.date, d.dob) = a.min_age
ORDER BY age;