SELECT r.year AS season,
COUNT(re.raceid) AS race_count,
SUM(re.points) AS points,
CONCAT(COUNT(CASE WHEN re.positiontext = '1' THEN 1 END), ' (', ROUND((COUNT(CASE WHEN re.positiontext = '1' THEN 1 END)::NUMERIC / COUNT(re.driverid)) * 100, 0), '%%', ')') AS wins,
CONCAT(COUNT(CASE WHEN re.positiontext IN ('1', '2', '3') THEN 1 END), ' (', ROUND((COUNT(CASE WHEN re.positiontext IN ('1', '2', '3') THEN 1 END)::NUMERIC / COUNT(re.driverid)) * 100, 0), '%%', ')') AS podium,
COUNT(CASE WHEN s.status != 'Finished' THEN 1 END) AS dnfs
FROM drivers d
JOIN results re ON re.driverid = d.driverid
JOIN races r ON re.raceid = r.raceid
JOIN status s ON s.statusid = re.statusid
WHERE d.driverid = %(sDriverId)s  AND r.year BETWEEN (SELECT MIN(year) FROM races) AND (SELECT MAX(year) FROM races)
GROUP BY r.year;