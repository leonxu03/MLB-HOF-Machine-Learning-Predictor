# count total number of players in the dataset
use ece356db_test;
SELECT count(*) from people;
 
# count nubmer of players in Hall of Fame
use ece356db_test;
SELECT * FROM halloffame;
# SELECT COUNT(DISTINCT playerID) AS players_in_hall_of_fame FROM halloffame;

# count the number of players inducted into the Hall of Fame
use ece356db_test;
SELECT COUNT(DISTINCT playerID) FROM halloffame WHERE inducted = 'Y';

SELECT * FROM allstarfull;
SELECT * FROM awardsplayers;
SELECT * FROM appearances;
SELECT * FROM batting;
SELECT * FROM pitching;
SELECT * FROM fieldingpost;

# get Task A feature set
SELECT 
    p.playerID,
    (SELECT COUNT(a.playerID) FROM allstarfull a WHERE a.playerID = p.playerID) AS allStarCount,
    (SELECT COUNT(ap.playerID) FROM awardsplayers ap WHERE ap.playerID = p.playerID) AS awardsCount,
    a.totalGamesBatting, a.totalGamesDefense, a.totalGamesPitching, a.totalGamesCatcher,
    b.totalHomeRuns, pitch.totalPitchingStrikeOuts, pitch.totalWins, f.totalFielderPutouts,
	CASE 
        WHEN EXISTS (SELECT 1 FROM halloffame hof WHERE p.playerID = hof.playerID) THEN 'True'
        ELSE 'False'
    END AS class
FROM 
    people p
LEFT JOIN (SELECT playerID, SUM(G_batting) as totalGamesBatting, SUM(G_defense) as totalGamesDefense, SUM(G_p) as totalGamesPitching,
    SUM(G_c) as totalGamesCatcher FROM appearances GROUP BY playerID) a ON p.playerID = a.playerID
LEFT JOIN (SELECT playerID, SUM(batting.HR) as totalHomeRuns FROM batting GROUP BY playerID) b ON p.playerID = b.playerID
LEFT JOIN (SELECT playerID, SUM(pitching.SO) as totalPitchingStrikeOuts, SUM(pitching.W) as totalWins FROM pitching GROUP BY playerID) 
    pitch ON p.playerID = pitch.playerID
LEFT JOIN (SELECT playerID, SUM(fielding.po) as totalFielderPutouts FROM fielding GROUP BY playerID) f ON p.playerID = f.playerID;

# get Task B feature set
SELECT 
    hof.playerID,
    (SELECT COUNT(a.playerID) FROM allstarfull a WHERE a.playerID = hof.playerID) AS allStarCount,
    (SELECT COUNT(ap.playerID) FROM awardsplayers ap WHERE ap.playerID = hof.playerID) AS awardsCount,
    a.totalGamesBatting, a.totalGamesDefense, a.totalGamesPitching, a.totalGamesCatcher,
    b.postHomeRuns, pitch.postPitchingStrikeOuts, pitch.postTotalWins, f.postFielderPutouts,
	CASE 
        WHEN hof.inducted = 'Y' THEN 'True'
        ELSE 'False'
    END AS class
FROM 
    (SELECT halloffame.playerID, CASE WHEN MAX(halloffame.inducted = 'Y') THEN 'Y' ELSE 'F' END AS inducted FROM halloffame GROUP by halloffame.playerID) as hof
LEFT JOIN (SELECT playerID, SUM(G_batting) as totalGamesBatting, SUM(G_defense) as totalGamesDefense, SUM(G_p) as totalGamesPitching, SUM(G_c) as totalGamesCatcher 
    FROM appearances GROUP BY playerID) a ON hof.playerID = a.playerID
LEFT JOIN (SELECT playerID, SUM(battingpost.HR) as postHomeRuns FROM battingpost GROUP BY playerID) b ON hof.playerID = b.playerID
LEFT JOIN (SELECT playerID, SUM(pitchingpost.SO) as postPitchingStrikeOuts, SUM(pitchingpost.W) as postTotalWins FROM pitchingpost GROUP BY playerID) pitch 
    ON hof.playerID = pitch.playerID
LEFT JOIN (SELECT playerID, SUM(fieldingpost.po) as postFielderPutouts FROM fieldingpost GROUP BY playerID) f ON hof.playerID = f.playerID;

