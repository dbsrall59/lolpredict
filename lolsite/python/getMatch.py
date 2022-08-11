from lolsite.python.myBinary import binarySearchtuple
import requests
from urllib import parse, request
import time
from datetime import datetime
import cx_Oracle as db
import random
import math
import numpy as np
import pandas as pd
import os
import random

def getRankNum(x):
    rankNum = 0
    if(x['tier'] == 'IRON'):
        rankNum = 10
    elif(x['tier'] == 'BRONZE'):
        rankNum = 20
    elif(x['tier'] == 'SILVER'):
        rankNum = 30
    elif(x['tier'] == 'GOLD'):
        rankNum = 40
    elif(x['tier'] == 'PLATINUM'):
        rankNum = 50
    elif(x['tier'] == 'DIAMOND'):
        rankNum = 60
    elif((x['tier'] == 'MASTER') | (x['tier'] == 'GRANDMASTER') | (x['tier'] == 'CHALLENGER')):
        rankNum = 70
    
    if(x['rank'] == 'I'):
        rankNum += 1
    elif(x['rank'] == 'II'):
        rankNum += 2
    elif(x['rank'] == 'III'):
        rankNum += 3
    elif(x['rank'] == 'IV'):
        rankNum += 4
        
    return rankNum

def setRankTier(x):
    tier = 'IRON'
    if(int(x / 10) == 2):
        tier = 'BRONZE'
    elif(int(x / 10) == 3):
        tier = 'SILVER'
    elif(int(x / 10) == 4):
        tier = 'GOLD'
    elif(int(x / 10) == 5):
        tier = 'PLATINUM'
    elif(int(x / 10) == 6):
        tier = 'DIAMOND'
    elif(int(x / 10) == 7):
        tier = 'MASTERUPPER'

    rank = 'IV'
    if(x % 10 == 1):
        rank = "I"
    elif(x % 10 == 2):
        rank = "II"
    elif(x % 10 == 3):
        rank = "III"

    return tier + ' ' + rank

def getMatchFromId(idList):
    with open('lolsite/apiKey/apikey.txt', 'r') as f:
        requestHeader = f.read()
    requestHeader = eval(requestHeader)
    
    LOCATION = 'C:' + os.environ['HOMEPATH'] + '\\instantclient_21_6'
    os.environ['PATH'] = LOCATION + ';' + os.environ['PATH']
    os.environ['NLS_LANG'] = 'KOREAN_KOREA.KO16MSWIN949'

    conn = db.connect('lolpredict','korhrd','127.0.0.1:1521')
    cursor = conn.cursor()

    matchCount = 100
    for id in idList:
        headerIndex = random.randint(0, len(requestHeader) - 1)

        nameUrl = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + id
        nameResult = requests.get(nameUrl, headers=requestHeader[headerIndex])
        nameCode = nameResult.status_code
        if(nameCode != 200):
            cursor.close()
            conn.close()
            return {"네임코드", nameCode}

        encryptUrl = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/" + nameResult.json()['id']
        encryptResult = requests.get(encryptUrl, headers=requestHeader[headerIndex])
        encryptCode = encryptResult.status_code
        if(encryptCode != 200):
            cursor.close()
            conn.close()
            return {"인크립트코드", encryptCode}

        encryptResult = encryptResult.json()
        isExist = False
        for i in encryptResult:
            if(i['queueType'] == 'RANKED_SOLO_5x5'):
                isExist = True
                ranktier = getRankNum(i)

                sql = """insert into userinfo select '{}', {} from dual
                    where not exists(
                        select 0
                        from userinfo
                        where username = '{}'
                    )
                    """.format(id, ranktier, id)
                cursor.execute(sql)

                sql = "update userinfo set ranktier = {} where username = '{}'".format(ranktier, id)
                cursor.execute(sql)
                conn.commit()
                break
        
        if(isExist == False):
            cursor.close()
            conn.close()
            return False


        puuidUrl = "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/" + nameResult.json()['puuid'] + "/ids?start=0&count={}".format(matchCount)
        puuidResult = requests.get(puuidUrl, headers=requestHeader[headerIndex])
        puuidCode = puuidResult.status_code
        if(puuidCode != 200):
            cursor.close()
            conn.close()
            return {"puuid코드", puuidCode}

        puuidResult = puuidResult.json()
        if(len(puuidResult) == 0):
            cursor.close()
            conn.close()
            return id

        sql = "select matchid from matchDetail where userName = '{}' order by matchid".format(id)
        cursor.execute(sql)
        searchedMatchList = np.array(cursor.fetchall())

        for matchid in puuidResult:
            searchResult = binarySearchtuple(matchid, searchedMatchList, 0)
            if(searchResult[0] == True):
                continue

            matchUrl = "https://asia.api.riotgames.com/lol/match/v5/matches/" + matchid
            matchResult = requests.get(matchUrl, headers=requestHeader[random.randint(0, len(requestHeader) - 1)])
            matchCode = matchResult.status_code
            if(matchCode != 200):
                continue

            matchResult = matchResult.json()
            startTime = matchResult['info']['gameStartTimestamp'] / 1000
            realTime = datetime.fromtimestamp(startTime).strftime("%y%m%d")
            if(realTime < "220524"):
                break

            if (matchResult['info']['queueId'] == 420):
                sql = """insert into matchinfo values('{}')""".format(matchResult['metadata']['matchId'])
                cursor.execute(sql)
                conn.commit()

                for i in matchResult['info']['participants']:
                    sql = """insert into matchDetail values(
                        '{}', '{}', {}, {}, {}, {}, {}, {}, {}, {}, 
                    {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, 
                    {}, {}, {}, {}, {}, {}, {}, {}, {})""".format(
                        matchResult['metadata']['matchId'],
                        i['summonerName'],
                        int(i['win']),
                        matchResult['info']['gameDuration'],
                        i['turretsLost'],
                        i['inhibitorsLost'],
                        i['turretTakedowns'],
                        i['inhibitorTakedowns'],
                        i['nexusTakedowns'],
                        i['bountyLevel'],
                        i['turretKills'],
                        i['deaths'],
                        i['damageDealtToTurrets'],
                        i['inhibitorKills'],
                        i['assists'],
                        i['kills'],
                        i['killingSprees'],
                        i['goldEarned'],
                        i['champExperience'],
                        i['champLevel'],
                        i['dragonKills'],
                        i['baronKills'],
                        i['totalDamageDealtToChampions'],
                        int(i['firstTowerKill']),
                        i['visionScore'],
                        i['neutralMinionsKilled'],
                        int(i['teamEarlySurrendered']),
                        i['totalTimeCCDealt'],
                        i['detectorWardsPlaced']
                    )
                    cursor.execute(sql)
                    conn.commit()
                conn.commit()

    cursor.close()
    conn.close()
    return True
        


        

    