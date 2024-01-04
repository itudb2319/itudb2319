SELECT c.name, 
r.round, 
SUM(res.points), 
con.name
FROM races r
JOIN results res ON r.raceId = res.raceId
JOIN constructors con ON res.constructorId = con.constructorId
JOIN circuits c ON r.circuitId = c.circuitId
WHERE con.constructorId = %(sConstructorId)s AND r.year = COALESCE(%(sYear)s, (SELECT MAX(r.year) FROM races r))
GROUP BY c.name, r.round, con.name
ORDER BY r.round;
