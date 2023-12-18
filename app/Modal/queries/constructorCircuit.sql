SELECT c.name, r.round, sum(res.points), con.name
FROM races r
JOIN results res ON r.raceId = res.raceId
JOIN constructors con ON res.constructorId = con.constructorId
JOIN circuits c ON r.circuitId = c.circuitId
WHERE con.constructorId = %(sConstructorId)s and EXTRACT(YEAR FROM r.date) = COALESCE(%(sYear)s, EXTRACT(YEAR FROM CURRENT_DATE))
GROUP BY c.name, r.round, r.year, con.name
ORDER BY r.round
