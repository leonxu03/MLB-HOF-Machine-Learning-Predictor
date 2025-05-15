SELECT 
    hof.playerID,
    (SELECT COUNT(a.playerID) FROM allstarfull a WHERE a.playerID = hof.playerID) AS allStarCount,
    (SELECT COUNT(ap.playerID) FROM awardsplayers ap WHERE ap.playerID = hof.playerID) AS awardsCount,
    a.totalGames,
    b.totalHomeRuns, b.totalHits, 
    pitch.totalPitchingStrikeOuts, pitch.totalPitchWins, 
    f.totalFielderPutouts,
    bPost.postHomeRuns, bPost.postHits, 
    pitchPost.postPitchingStrikeOuts, pitchPost.postTotalWins, 
    fPost.postFielderPutouts,
	CASE 
        WHEN hof.inducted = 'Y' THEN 'True'
        ELSE 'False'
    END AS class
FROM 
    (SELECT halloffame.playerID, CASE WHEN MAX(halloffame.inducted = 'Y') THEN 'Y' ELSE 'F' END AS inducted FROM halloffame GROUP by halloffame.playerID) as hof
LEFT JOIN (SELECT playerID, MAX(yearID) as lastSeasonPlayed, MIN(yearID) as firstSeasonPlayed, SUM(G_batting) as totalGamesBatting,  SUM(G_p) as totalGamesPitching, 
    SUM(G_all) as totalGames FROM appearances GROUP BY playerID) a ON hof.playerID = a.playerID
LEFT JOIN (SELECT playerID, SUM(batting.HR) as totalHomeRuns, SUM(batting.H) as totalHits FROM batting GROUP BY playerID) b ON hof.playerID = b.playerID
LEFT JOIN (SELECT playerID, SUM(pitching.SO) as totalPitchingStrikeOuts, SUM(pitching.W) as totalPitchWins FROM pitching GROUP BY playerID) pitch 
    ON hof.playerID = pitch.playerID
LEFT JOIN (SELECT playerID, SUM(fielding.PO) as totalFielderPutouts, SUM(fielding.A) as totalFielderAssists, SUM(fielding.E) as totalFielderErrors, 
    AVG(fielding.ZR) as avgZR FROM fielding GROUP BY playerID) f ON hof.playerID = f.playerID
LEFT JOIN (SELECT playerID, SUM(battingpost.HR) as postHomeRuns, SUM(battingpost.H) as postHits FROM battingpost GROUP BY playerID) bPost 
    ON hof.playerID = bPost.playerID
LEFT JOIN (SELECT playerID, SUM(pitchingpost.SO) as postPitchingStrikeOuts, SUM(pitchingpost.W) as postTotalWins FROM pitchingpost GROUP BY playerID) pitchPost 
    ON hof.playerID = pitchPost.playerID
LEFT JOIN (SELECT playerID, SUM(fieldingpost.po) as postFielderPutouts FROM fieldingpost GROUP BY playerID) fPost ON hof.playerID = fPost.playerID;

