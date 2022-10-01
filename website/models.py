from django.db import models

# Create your models here.

class Player(models.Model):
    name = models.CharField(max_length=20)
    coins = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)


class Game(models.Model):
    ownerName = models.CharField(max_length=100)
    ownerChoice = models.CharField(max_length=100, default="")
    joinerName = models.CharField(max_length=100)
    joinerChoice = models.CharField(max_length=100, default="")
    side = models.CharField(max_length=100, default="")
    betAmount = models.IntegerField()
    winner = models.CharField(max_length=100, default="")
    status = models.CharField(max_length=100)
