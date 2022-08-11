import numpy as np
import cx_Oracle as db
import pandas as pd
import os
import joblib

def predict(idList):
    rankList = [11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 41, 42, 43, 44, 51, 52, 53, 54, 61, 62, 63, 64, 71]

    LOCATION = 'C:' + os.environ['HOMEPATH'] + '\\instantclient_21_6'
    os.environ['PATH'] = LOCATION + ';' + os.environ['PATH']
    os.environ['NLS_LANG'] = 'KOREAN_KOREA.KO16MSWIN949'

    countInf = 0.872
    countMax = 20

    conn = db.connect('lolpredict','korhrd','127.0.0.1:1521')
    cursor = conn.cursor()

    rankMeanAll = pd.read_csv('lolsite/data/rankMean.csv', encoding='CP949')

    x_dataList = []
    for id in idList:
            sql ="""select 
                        time, 
                        turretsLost, 
                        inhibitorsLost,
                        turretTakedowns, 
                        inhibitorTakedowns, 
                        nexusTakedowns,
                        bountyLevel,
                        turretKills, 
                        deaths, 
                        damageDealtToTurrets,
                        inhibitorKills, 
                        assists, 
                        kills, 
                        killingSprees, 
                        goldEarned,
                        champExperience, 
                        champLevel, 
                        dragonKills, 
                        baronKills,
                        totalDamageDealtToChampions, 
                        firstTowerKill, 
                        visionScore,
                        neutralMinionsKilled,
                        totalTimeCCDealt,
                        detectorWardsPlaced
                    from matchDetail where userName = '{}'""".format(id)

            cursor.execute(sql)

            matchList = cursor.fetchall()
            colname = cursor.description

            matchColumn=[]
            for i in colname:
                matchColumn.append(i[0])

            df = pd.DataFrame(matchList, columns=matchColumn)
            dfmean = df.mean().to_numpy().reshape(1, -1)

            sql = "select ranktier from userinfo where username = '{}'".format(id)
            cursor.execute(sql)
            userRank = cursor.fetchall()[0][0]

            matchCount = len(df)
            if(matchCount < countMax):
                rankMean = rankMeanAll[rankMeanAll['rank'] == userRank]
                rankMean = rankMean.drop(['win', 'matchCount', 'rank'], axis='columns').to_numpy()

                percentige = np.power(countInf, matchCount)
                dfmean = dfmean * (1-dfmean) + rankMean * percentige

            x_dataList.append([id, userRank, np.log1p(dfmean.astype('float'))])

    
    cursor.close()
    conn.close()
    
    predictList = []
    for x_data in x_dataList:
        for ranktier in rankList:
            rankModel = joblib.load('lolsite/model/model_rank{}.h5'.format(ranktier))
            predictResult = {'id' : x_data[0], 'currentRank' : x_data[1], 'ranktier' : ranktier, 'result' : rankModel.predict(x_data[2])[0]}
            predictList.append(predictResult)

    return predictList


