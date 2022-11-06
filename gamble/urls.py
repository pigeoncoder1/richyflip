from website.views import goToLogin,startGame,calculateWin,lobby,stats,joinGame,createdGame,doLogin,seeOutcome,checkHaveCoins,checkIsOwner,lookUpPlayer,createUser,goToCreateUser,hallOfFame,shop,addTokens
from django.contrib import admin
from django.urls import path
wins = 0
losses = 0
#reminder to add all urls to views.py list
#^lol

urlpatterns = [
    path('', goToLogin, name=""),
    path('doLogin', doLogin, name="doLogin"),
    path('lobby', lobby, name="lobby"),
    path('joinGame/<int:id>', joinGame, name='joinGame'),
    path('stats', stats, name="stats"),
    path('startGame', startGame, name='startGame'),
    path('calculateWin/<int:id>', calculateWin, name='calculateWin'),
    path('createdGame', createdGame, name='createdGame'),
    path('seeOutcome/<int:id>', seeOutcome, name="seeOutcome"),
    path('checkHaveCoins', checkHaveCoins, name="checkHaveCoins"),
    path('checkIsOwner/<int:id>', checkIsOwner, name="checkIsOwner"),
    path('lookUpPlayer', lookUpPlayer, name="lookUpPlayer"),
    path('createUser', createUser, name="createUser"),
    path('goToCreateUser',goToCreateUser, name="goToCreateUser"),
    path('hallOfFame', hallOfFame, name="hallOfFame"),
    path('shop', shop, name='shop'),
    path('addTokens',addTokens,name="addTokens")
]
