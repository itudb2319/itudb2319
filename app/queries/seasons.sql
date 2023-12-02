SELECT r.name, TO_CHAR(r.date, 'dd/mm/yyyy'), c.name, c.location, c.country  FROM races as r
JOIN circuits AS c
    ON r.circuitId = c.circuitId
    AND r.year = %(sYear)s
ORDER BY r.date;
    
