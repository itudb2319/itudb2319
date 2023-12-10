SELECT d.forename, d.surname,
(SELECT CONCAT(MIN(r.year), ' - ', MAX(r.year))
FROM races r JOIN results re ON re.raceid = r.raceid
WHERE re.positiontext = '1' AND re.driverid = d.driverid) AS seasons,
COUNT (re.driverid) AS ENTRY, 
COUNT(CASE WHEN re.positiontext = '1' THEN 1 ELSE NULL END) AS total_wins,
ROUND((COUNT(CASE WHEN re.positiontext = '1' THEN 1 ELSE NULL END)::NUMERIC / COUNT (re.driverid))::NUMERIC * 100, 2) AS win_rate
FROM drivers d JOIN results re ON d.driverid = re.driverid 
GROUP BY d.forename, d.surname, d.driverid
ORDER BY total_wins 
DESC;