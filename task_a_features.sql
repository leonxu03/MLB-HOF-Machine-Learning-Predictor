SELECT 
    p.playerID,
    (SELECT COUNT(allStar.playerID) FROM allstarfull allStar WHERE allStar.playerID = p.playerID) AS allStarCount,
    (SELECT COUNT(ap.playerID) FROM awardsplayers ap WHERE ap.playerID = p.playerID) AS awardsCount,
    a.totalGames,
    b.totalHomeRuns, b.totalHits, pitch.totalPitchingStrikeOuts, pitch.totalPitchWins, f.totalFielderPutouts,
    CASE 
		WHEN a.lastSeasonPlayed - a.firstSeasonPlayed >= 10 and a.lastSeasonPlayed < 2018 THEN 1
        ELSE 0
    END AS eligible, -- HOF Eligibility: At least 10 seasons played, and has retired at least 5 years ago
    CASE 
        WHEN EXISTS (SELECT 1 FROM halloffame hof WHERE p.playerID = hof.playerID) THEN 'True'
        ELSE 'False'
    END AS class
FROM 
    people p
LEFT JOIN (SELECT playerID, MAX(yearID) as lastSeasonPlayed, MIN(yearID) as firstSeasonPlayed, SUM(G_batting) as totalGamesBatting, 
    SUM(G_p) as totalGamesPitching, SUM(G_all) as totalGames FROM appearances GROUP BY playerID) a ON p.playerID = a.playerID
LEFT JOIN (SELECT playerID, SUM(batting.HR) as totalHomeRuns, SUM(batting.H) as totalHits FROM batting GROUP BY playerID) b ON p.playerID = b.playerID
LEFT JOIN (SELECT playerID, SUM(pitching.SO) as totalPitchingStrikeOuts, SUM(pitching.W) as totalPitchWins FROM pitching GROUP BY playerID) pitch 
    ON p.playerID = pitch.playerID
LEFT JOIN (SELECT playerID, SUM(fielding.PO) as totalFielderPutouts, SUM(fielding.A) as totalFielderAssists, SUM(fielding.E) as totalFielderErrors, AVG(fielding.ZR) 
    as avgZR FROM fielding GROUP BY playerID) f ON p.playerID = f.playerID;


