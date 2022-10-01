from website.views import login,startGame,calculateWin,lobby,stats,joinGame,createdGame,doLogin,seeOutcome,checkHaveCoins
from django.contrib import admin
from django.urls import path
wins = 0
losses = 0
#reminder to add all urls to views.py list

urlpatterns = [
    path('', login, name=""),
    path('doLogin', doLogin, name="doLogin"),
    path('lobby', lobby, name="lobby"),
    path('joinGame/<int:id>', joinGame, name='joinGame'),
    path('stats', stats, name="stats"),
    path('startGame', startGame, name='startGame'),
    path('calculateWin/<int:id>', calculateWin, name='calculateWin'),
    path('createdGame', createdGame, name='createdGame'),
    path('seeOutcome/<int:id>', seeOutcome, name="seeOutcome"),
    path('checkHaveCoins', checkHaveCoins, name="checkHaveCoins"),
]
