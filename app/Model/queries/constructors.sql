SELECT c.name, c.nationality, sum(cs.points) AS totalPoints, c.constructorid FROM constructorstandings cs
    JOIN constructors c ON cs.constructorid = c.constructorid
    GROUP BY c.constructorid, c.nationality, c.name;
