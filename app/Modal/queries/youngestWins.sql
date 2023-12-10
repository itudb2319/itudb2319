SELECT d.forename, 
d.surname, 
a.min_age as age, 
a.season, 
r.name
FROM races r JOIN results re ON re.raceid = r.raceid 
JOIN drivers d ON d.driverid = re.driverid 
JOIN (SELECT re.driverid, 
        MIN(AGE(r.date, d.dob)) as min_age, 
        MIN(r.year) as season,
        re.positiontext
    FROM races r JOIN results re ON re.raceid = r.raceid 
    JOIN drivers d ON d.driverid = re.driverid 
    WHERE re.positiontext = '1'
    GROUP BY re.driverid, re.positiontext
)a ON d.driverid = a.driverid 
AND AGE(r.date, d.dob) = a.min_age AND re.positiontext = a.positiontext
ORDER BY age;