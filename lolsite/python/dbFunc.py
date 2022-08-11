import cx_Oracle as db
import os
import bcrypt

def startDB():
    LOCATION = 'C:' + os.environ['HOMEPATH'] + '\\instantclient_21_6'
    os.environ['PATH'] = LOCATION + ';' + os.environ['PATH']
    os.environ['NLS_LANG'] = 'KOREAN_KOREA.KO16MSWIN949'

    conn = db.connect('lolpredict','korhrd','127.0.0.1:1521')
    cursor = conn.cursor()

    return conn, cursor

def endDB(conn, cursor):
    cursor.close()
    conn.close()

def dbJoin(joinId, joinPassword, joinNickname):
    conn, cursor = startDB()

    sql = "select saltkey from saltTable"
    cursor.execute(sql)
    saltKey = cursor.fetchall()[0][0]

    joinPassword = bcrypt.hashpw(joinPassword.encode('utf-8'), saltKey.encode()).decode('utf-8')

    sql = """insert into 
                siteUserInfo(siteUserID, siteUserName, sitePassword, NickName) 
                values 
                (siteUserIdSeq.NEXTVAL, '{}', '{}', '{}')""".format(joinId, joinPassword, joinNickname)
    
    result = 0
    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        msg = str(e)
        result = msg[msg.find('.') + 1 : msg.find('_')]

    endDB(conn, cursor)
    return result

def dbLogin(loginId, loginPassword):
    conn, cursor = startDB()

    sql = "select saltkey from saltTable"
    cursor.execute(sql)
    saltKey = cursor.fetchall()[0][0]

    loginPassword = bcrypt.hashpw(loginPassword.encode('utf-8'), saltKey.encode()).decode('utf-8')

    sql = """select siteUserName, sitePassword, nickName 
                from siteUserInfo
                where siteUserName = '{}' and sitePassword = '{}'""".format(loginId, loginPassword)
    
    cursor.execute(sql)
    result = cursor.fetchall()

    endDB(conn, cursor)
    if(len(result) == 0):
        return False
    return {"id" : result[0][0], "nickName" : result[0][2]}    

def getBoard():
    conn, cursor = startDB()

    sql = """select boardID, title, contentSrc, siteUserName, viewCount, goodCount, badCount
                from board B
                inner join siteUserInfo A on B.siteUserID = A.siteUserID"""
    cursor.execute(sql)
    contents = cursor.fetchall()

    endDB(conn, cursor)
    return contents

def writeBoard(siteUserName, title, contentSrc):
    conn, cursor = startDB()

    sql = """insert into board
                values (boardidseq.nextval,
                (select siteuserid
                from siteuserinfo
                where siteuserinfo.siteusername = '{}'),
                '{}', '{}', 1, 0, 0)""".format(siteUserName, title, contentSrc)

    result = 0
    
    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        msg = str(e)
        result = msg[msg.find('.') + 1 : msg.find('_')]

    endDB(conn, cursor)
    return result

def viewContent(boardId):
    conn, cursor = startDB()

    sql = """select boardID, title, contentSrc, siteUserName, viewCount, goodCount, badCount
                from board B
                inner join siteUserInfo A on B.siteUserID = A.siteUserID
                where boardID = {}""".format(boardId)
    cursor.execute(sql)
    content = cursor.fetchall()[0]

    sql = """select C.siteusername, A.replyContent, D.siteusername
                from reply A
                inner join board B on A.boardid = B.boardid
                inner join siteuserinfo C on A.siteuserid = C.siteuserid
                left outer join siteuserinfo D on A.replyto = D.siteuserid
                where B.boardid = {}""".format(boardId)
    cursor.execute(sql)
    replies = cursor.fetchall()
    
    endDB(conn, cursor)

    if(len(content) == 0):
        return False, False
    return content, replies
    
def writeReply(boardId, userId, content, replyTo):
    conn, cursor = startDB()

    sql = """insert into reply(replyId, siteuserId, boardId, replyContent, replyTo)
                select replyIdSeq.nextval, A.siteuserid, {}, '{}',
                    (select siteuserid
                    from siteuserinfo B
                    where B.siteusername = '{}')
                from siteuserinfo A
                where A.siteusername = '{}'""".format(boardId, content, replyTo, userId)

    result = 0
    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        msg = str(e)
        result = msg[msg.find('.') + 1 : msg.find('_')]

    endDB(conn, cursor)
    return result