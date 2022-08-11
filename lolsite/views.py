from django.shortcuts import render
from django.http import HttpRequest
from lolsite.python.getMatch import getMatchFromId, setRankTier
from lolsite.python.predict import predict
from lolsite.python.predictMean import predictmean
import lolsite.python.dbFunc as dbFunc
import pandas as pd

# Create your views here.
def home(request):
    return render(request, 'lolsite/home.html', {})

def search(request):
    if (request.method == 'POST'):
        form = request.POST
        searchidList = []
        for i in range(5):
            searchid = form['search_id{}'.format(i)]
            if(len(searchid) > 0):
                searchidList.append(searchid)

        searchResult = getMatchFromId(searchidList)

        if(searchResult == True):
            predictResult = predict(searchidList)
            meanRanktier, meanResult = predictmean(predictResult)
            
            meanRank = setRankTier(meanRanktier)
            meanResult['ranktier'] = meanResult['ranktier'].apply(lambda x : setRankTier(x))
            result = {"meanRank" : meanRank, "meanResult" : meanResult.to_numpy()}
        else:
            result = {"wow" : searchResult}
            return render(request, 'lolsite/accessdenied.html', result)

    return render(request, 'lolsite/searchResult.html', result)

def join(request):
    return render(request, 'lolsite/join.html', {})

def dbjoin(request):

    if (request.method == 'POST'):
        form = request.POST
        joinId = form['join_id']
        joinPassword = form['join_password']
        joinNickname = form['join_nickname']

        if(joinNickname == ""):
            joinNickname = joinId

        joinResult = dbFunc.dbJoin(joinId, joinPassword, joinNickname)
        if(joinResult == 0):
            result = {"joinId" : joinId}
            return render(request, 'lolsite/joinSuccess.html', result)

        else:
            result = {"colName" : joinResult}
            return render(request, 'lolsite/joinFail.html', result)

    return render(request, 'lolsite/accessdenied.html', {})
        
def login(request):
    return render(request, 'lolsite/login.html', {})

def dblogin(request):
    if (request.method == 'POST'):
        form = request.POST
        loginId = form['login_id']
        loginPassword = form['login_password']

        loginResult = dbFunc.dbLogin(loginId, loginPassword)
        
        if(loginResult == False):
            return render(request, 'lolsite/accessdenied.html')

        resultRender = render(request, 'lolsite/anySuccess.html', {"destination" : 'home'})
        resultRender.set_cookie("ID", loginResult["id"],)
        resultRender.set_cookie("nickName", loginResult['nickName'])
        return resultRender

    return render(request, 'lolsite/accessdenied.html', {})

def logout(request):
    resultRender = render(request, 'lolsite/anySuccess.html', {"destination" : 'home'})
    if(request.COOKIES['ID'] != None):
        resultRender.delete_cookie('ID')
        resultRender.delete_cookie('nickName')
        
    return resultRender

def board(request):
    result = dbFunc.getBoard()
    return render(request, 'lolsite/board.html', {"boardList" : result})

def writeBoard(request):
    return render(request, 'lolsite/writeboard.html', {})

def writeComplete(request):
    if (request.method == 'POST'):
        form = request.POST
        writeboardTitle = form['writeboard_title']
        writeboardContent = form['writeboard_content']
        
        result = dbFunc.writeBoard(request.COOKIES['ID'], writeboardTitle, writeboardContent)
        if(result != 0):
            return render(request, 'lolsite/accessdenied.html', {"wow" : result})
        return render(request, 'lolsite/anySuccess.html', {"destination" : 'board'})

    return render(request, 'lolsite/accessdenied.html', {})

def search2(request):
    predictResult = {"meanRank" : "examTier", "meanResult" : pd.read_csv('examDF.csv', encoding='CP949').to_numpy()}

    return render(request, 'lolsite/searchResult.html', predictResult)

def boardcontent(request, boardid):
    content, replies = dbFunc.viewContent(boardid)
    
    if(content == False):
        return render(request, 'lolsite/accessdenied.html', {})
    return render(request, 'lolsite/boardContent.html', {"content" : content, "replyList" : replies})

def writereply(request, boardid):
    if (request.method == 'POST'):
        form = request.POST

        userId = request.COOKIES['ID']
        content = form['reply_content']
        replyTo = form['reply_To']

        result = dbFunc.writeReply(boardid, userId, content, replyTo)

        if(result == 0):
             return render(request, 'lolsite/anySuccess.html', {"destination" : 'boardcontent/{}'.format(boardid)})
        
    return render(request, 'lolsite/accessdenied.html', {})
