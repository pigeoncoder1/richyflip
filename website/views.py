from django.shortcuts import render,redirect, get_object_or_404
from django.db.models import Q, Max
from django.http import HttpResponse
import random
from .models import Player, Game


def goToLogin(request):
    return render(request, "website/login.html")

def doLogin(request):
    if Player.objects.filter(name=request.POST['username'],password=request.POST['password']).exists():
        request.session['username'] = request.POST['username']
        request.session['password'] = request.POST['password']
        return redirect('/lobby')
    else:
        return render(request, "website/login.html", {'CreateUser':"User does not exist: Try Creating a User Instead: "})

def goToCreateUser(request):
    return render(request, "website/createUser.html")

def createUser(request):
    if not Player.objects.filter(name=request.POST['username']).exists():
        newUser = Player()
        newUser.name = request.POST['username']
        newUser.password = request.POST['password']
        newUser.coins = 100
        newUser.save()
        return redirect('/')

    elif len(request.POST['username']) < 3:
        return render(request, "website/error.html", {'message': 'Username has to be longer than 3 letters', 'return':'', 'goTo':'login page'})

    elif Player.objects.filter(name=request.POST['username']).exists():
        return render(request, "website/error.html", {'message': 'Username already taken', 'return':'', 'goTo':'login page'})

def lobby(request):
    username = request.session['username']
    latestGames = Game.objects.order_by('-pk')
    player, created = Player.objects.get_or_create(name=username, defaults={"name":username,"coins":0,"wins":0,"losses":0})

    context = {'username': username, 'wins': player.wins, 'losses': player.losses, 'coins': player.coins, 'games': latestGames}
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
    player.coins -= int(request.session['betAmount'])
    player.save()

    game = Game()
    game.ownerName = request.session['username']
    game.ownerChoice = request.session['choice']
    game.betAmount = int(request.session['betAmount'])
    game.status = "open"
    game.save()
    return redirect('/lobby')

def seeOutcome(request,id):
    game = Game.objects.get(pk=id)
    context = {'winner':game.winner,'ownerName':game.ownerName,'ownerChoice':game.ownerChoice,'joinerName':game.joinerName,"joinerChoice":game.joinerChoice,'betAmount':game.betAmount,'status':game.status, 'side':game.side}
    return render(request, "website/seeOutcome.html", context)

def checkHaveCoins(request):
    if int(Player.objects.get(name=request.session['username']).coins) < int(request.POST['betAmount']):
        return render(request, "website/error.html", {'message':"Not enough cash",'return':'lobby','goTo':'lobby'})
    else:
        request.session['betAmount'] = request.POST['betAmount']
        request.session['choice'] = request.POST['choice']
        return redirect('/createdGame')

def checkIsOwner(request,id):
    gameOwner = Game.objects.get(pk=id).ownerName
    if gameOwner == request.session['username']:
        return render(request, "website/error.html", {'message':'Cannot join yourself goofy ahh.','return':'lobby','goTo':'lobby'})
    elif int(Player.objects.get(name=request.session['username']).coins) < Game.objects.get(pk=id).betAmount:
        return render(request, "website/error.html", {'message':"Not enough cash",'return':'lobby','goTo':'lobby'})
    else:
        return calculateWin(request,id)

def lookUpPlayer(request):
    playerName = request.POST['username']
    if Player.objects.filter(name=playerName).exists():
        player = Player.objects.get(name=playerName)
        return render(request, "website/lookUpPlayer.html", {'name':player.name,'coins':player.coins,'wins':player.wins,'losses':player.losses})
    else:
        return render(request, "website/error.html", {'message':'Player does not exist... yet?','return':'lobby','goTo':'lobby'})

def hallOfFame(request):
    coinsOrder = Player.objects.order_by('coins')
    richestPlayerCoins = coinsOrder[len(coinsOrder) - 1].coins
    richestPlayer = coinsOrder[len(coinsOrder) - 1].name
    return render(request, "website/hallOfFame.html", {'richestPlayer':richestPlayer,'richestPlayerCoins':richestPlayerCoins})

def shop(request):
    return render(request, "website/shop.html")

def addTokens(request):
    player = Player.objects.get(name=request.session['username'])
    if player.coins < (int(request.POST['negatives']) * 5) + (int(request.POST['positives']) * 5):
        return render(request, "website/error.html", {'message':"Not enough cash",'return':'lobby','goTo':'lobby'})
    else:
        player.positives += int(request.POST['positives'])
        player.negatives += int(request.POST['negatives'])
        player.coins -= int(request.POST['negatives']) * 5 #this is the cost
        player.coins -= int(request.POST['positives']) * 5
        player.save()
        return redirect('/lobby')