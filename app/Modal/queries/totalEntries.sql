SELECT d.forename, 
d.surname, 
COUNT(re.driverid) AS Count 
FROM drivers d JOIN results re ON d.driverid = re.driverid 
GROUP BY d.forename, d.surname 
ORDER BY count 
DESC;