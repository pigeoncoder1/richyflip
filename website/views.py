from django.shortcuts import render,redirect, get_object_or_404
from django.db.models import Q, Max
from django.http import HttpResponse
import random
from .models import Player, Game

print("hi")
def login(request):
    return render(request, "website/login.html")

def doLogin(request):
    request.session['username'] = request.POST['username']
    return redirect('/lobby')

def lobby(request):

    username = request.session['username']
    latestGames = Game.objects.order_by('-pk')
    coinsOrder = Player.objects.order_by('coins')
    mostCoins = coinsOrder[len(coinsOrder)-1].coins
    mostCoinsName = coinsOrder[len(coinsOrder)-1].name
    player, created = Player.objects.get_or_create(name=username, defaults={"name":username,"coins":0,"wins":0,"losses":0})

    context = {'username': username, 'wins': player.wins, 'losses': player.losses, 'coins': player.coins, 'games': latestGames, 'mostCoinsName':mostCoinsName,'mostCoins':mostCoins}
    return render(request, "website/lobby.html", context)

def joinGame(request,id):
    game = get_object_or_404(Game, pk=id)
    owner = game.ownerName
    ownerChoice = game.ownerChoice
    you = request.session['username']
    betAmount = game.betAmount
    if ownerChoice == "Tix":
        yourChoice = "Bux"
    else:
        yourChoice = "Tix"

    context = {'owner':owner,"ownerChoice":ownerChoice,"you":you, "betAmount":betAmount,"yourChoice":yourChoice,'gameid':game.id}
    return render(request, "website/joinDetails.html",context)

def stats(request):
    player = Player.objects.get(name=request.session['username'])
    pastGames = Game.objects.filter(Q(ownerName=request.session['username']) | Q(joinerName=request.session['username']))
    pastGames = pastGames.filter(status="closed")

    context = {'username': player.name, 'wins': player.wins, 'losses': player.losses, 'coins': player.coins, 'pastGames':pastGames}
    return render(request, "website/stats.html", context)

def startGame(request):
    username = request.session['username']
    context = {'name': username}
    return render(request, "website/game.html", context)

def calculateWin(request,id):
    options = ['Tix', 'Bux']
    game = get_object_or_404(Game, pk=id)
    #parameters
    ownerName = game.ownerName
    betAmount = game.betAmount
    ownerChoice = game.ownerChoice
    joinerName = request.session['username']
    game.joinerName = joinerName

    joiner = Player.objects.get(name=joinerName)
    owner = Player.objects.get(name=ownerName)

    joiner.coins -= betAmount

    #funny
    if ownerChoice == options[0]:
        joinerChoice = options[1]
    else:
        joinerChoice = options[0]
    outcome = options[random.randint(0, 1)]
    side = outcome
    if outcome == ownerChoice:
        outcome = ownerName
        owner.wins += 1
        owner.coins += (betAmount * 2)
        joiner.losses += 1
    else:
        outcome = joinerName
        joiner.wins += 1
        joiner.coins += (betAmount * 2)
        owner.losses += 1

    # changes
    game.joinerChoice = joinerChoice
    game.status = "closed"
    game.winner = outcome
    game.side = side

    #saves
    game.save()
    joiner.save()
    owner.save()

    context = {'side': side, 'outcome': outcome, 'ownerName':ownerName, 'joinerName':joinerName,"betAmount":betAmount, 'joinerChoice':joinerChoice,'ownerChoice':ownerChoice}
    return render(request, "website/gameresult.html", context)

def createdGame(request):
    player = Player.objects.get(name=request.session['username'])
    player.coins -= int(request.POST['betAmount'])
    player.save()

    game = Game()
    game.ownerName = request.session['username']
    game.ownerChoice = request.POST['choice']
    game.betAmount = request.POST['betAmount']
    game.status = "open"
    game.save()
    return redirect('/lobby')

def seeOutcome(request,id):
    game = Game.objects.get(pk=id)
    context = {'winner':game.winner,'ownerName':game.ownerName,'ownerChoice':game.ownerChoice,'joinerName':game.joinerName,"joinerChoice":game.joinerChoice,'betAmount':game.betAmount,'status':game.status, 'side':game.side}
    return render(request, "website/seeOutcome.html", context)

def checkHaveCoins(request):
    if int(Player.objects.get(name=request.session['username']).coins) < int(request.POST['betAmount']):
        return redirect('/lobby')
    else:
        return redirect('/createdGame')