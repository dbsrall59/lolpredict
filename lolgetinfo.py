import requests
from urllib import parse
import time
from datetime import datetime
import cx_Oracle as db
import random
import math
import os

def binarySearchAsc(mItem, mList):
    
    startIndex = 0
    endIndex = len(mList) - 1
    
    while(startIndex <= endIndex):
        target = int((startIndex + endIndex) / 2)
        
        if(mItem == mList[target]):
            return [True, target]
        elif(mItem < mList[target]):
            endIndex = target - 1
        else:
            startIndex = target + 1
            
    if(endIndex == -1):
        return [False, startIndex]
    if(startIndex > endIndex):
        return [False, startIndex]
    return [False, target]

def binarySearchtuple(mItem, mList, key):

    startIndex = 0
    endIndex = len(mList) - 1
    
    while(startIndex <= endIndex):
        target = int((startIndex + endIndex) / 2)
        
        if(mItem == mList[target][key]):
            return [True, target]
        elif(mItem < mList[target][key]):
            endIndex = target - 1
        else:
            startIndex = target + 1
            
    if(endIndex == -1):
        return [False, startIndex]
    if(startIndex > endIndex):
        return [False, startIndex]
    return [False, target]

LOCATION = 'C:' + os.environ['HOMEPATH'] + '\\instantclient_21_6'
os.environ['PATH'] = LOCATION + ';' + os.environ['PATH']
os.environ['NLS_LANG'] = 'KOREAN_KOREA.KO16MSWIN949'

#테이블 3900 최대 117000 30
tablesize = 3900

conn = db.connect('lolpredict', 'korhrd', '163.152.224.168:1521')
cursor = conn.cursor()

sql = 'select * from userinfo where isComplete = 0'
cursor.execute(sql)
userList = cursor.fetchall()

sql = 'select matchid from matchinfo order by matchid'
cursor.execute(sql)
matchList = cursor.fetchall()

requestHeader = {
    
}

maxlength = 0
while(len(userList)):
    i0 = random.randint(0, len(userList) - 1)
    
    isnotFound = False
    nameUrl = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + userList[i0][0]
    nameCode = 0
    while(nameCode != 200):
        puuid = requests.get(nameUrl, headers=requestHeader)
        nameCode = puuid.status_code
        time.sleep(2)
        print(puuid.status_code)
            
        if(nameCode == 404):
            isnotFound = True
            break
    
    if(isnotFound == True):
        sql = "update userinfo SET iscomplete = 1 where username = '{}'".format(userList[i0][0])
        cursor.execute(sql)
        conn.commit()
        continue
    
    puuidUrl = "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/" + puuid.json()['puuid'] + "/ids?start=0&count=100"
    puuidCode = 0
    while(puuidCode != 200):
        puuidResult = requests.get(puuidUrl, headers=requestHeader)
        puuidCode = puuidResult.status_code
        time.sleep(2)
        print(puuidResult.status_code)
        
        if(nameCode == 404):
            isnotFound = True
            break
    
    if(isnotFound == True):
        sql = "update userinfo SET iscomplete = 1 where username = '{}'".format(userList[i0][0])
        cursor.execute(sql)
        conn.commit()
        continue
        
    for matchid in puuidResult.json():
        searchMatch = binarySearchtuple(matchid, matchList, 0)
        if searchMatch[0] == True:
            continue
        
        matchUrl = "https://asia.api.riotgames.com/lol/match/v5/matches/" + matchid
        matchCode = 0
        while(matchCode != 200):
            matchResult = requests.get(matchUrl, headers=requestHeader)
            matchCode = matchResult.status_code
            time.sleep(2)
            print(matchResult.status_code)
            
        for user in matchResult.json()['info']['participants']:
            searchUser = binarySearchtuple(user['summonerName'], userList, 0)
            if searchUser[0] == True:
                continue
                
            sql = "insert into userInfo values('{}', {})".format(user['summonerName'], 0)
            
            try:
                cursor.execute(sql)
                conn.commit()
            except:
                continue
        
        longjson = str(matchResult.json())
        longjson = longjson.replace("'", "\\\"")
        splitjson = []
        for i in range(math.ceil(len(longjson) / tablesize)):
            splitjson.append(longjson[i * tablesize : (i + 1) * tablesize])
        
        sql = "insert into matchInfo(matchid"
        for i in range(len(splitjson)):
            sql += ", matchjson{}".format(i)
        sql += ") values('{}'".format(matchid)
        for i in range(len(splitjson)):
            sql += ", '{}'".format(splitjson[i])
        sql += ')'
            
        try:
            cursor.execute(sql)
            conn.commit()
        except:
            continue
        
    sql = "update userinfo SET iscomplete = 1 where username = '{}'".format(userList[i0][0])
    cursor.execute(sql)
    conn.commit()
    
    sql = 'select * from userinfo where isComplete = 0 order by username'
    cursor.execute(sql)
    userList = cursor.fetchall()
    
    sql = 'select matchid from matchinfo order by matchid'
    cursor.execute(sql)
    matchList = cursor.fetchall()