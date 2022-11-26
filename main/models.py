from django.db import models
from django.contrib.auth.models import AbstractUser


class Info(models.Model):
    logo = models.ImageField(upload_to='info/')
    bio = models.TextField()
    phone = models.IntegerField()
    email = models.CharField(max_length=215)
    insta = models.URLField()
    tg = models.URLField()
    fb = models.URLField()
    yt = models.URLField()
    tw = models.URLField()


class Ads(models.Model):
    logo = models.ImageField(upload_to='ads/')
    url = models.URLField()


class Slider(models.Model):
    img = models.ImageField(upload_to='slider/')
    title = models.CharField(max_length=210)
    text = models.TextField(null=True, blank=True)


class Report(models.Model):
    img = models.ImageField(upload_to='report/', null=True, blank=True)
    video = models.FileField(upload_to='report/', null=True, blank=True)
    date = models.DateField()
    name = models.CharField(max_length=210)


class News(models.Model):
    img = models.ImageField(upload_to='news/')
    text = models.TextField()
    title = models.CharField(max_length=210)


class League(models.Model):
    name = models.CharField(max_length=210)
    logo = models.ImageField(upload_to='league/')


class Club(models.Model):
    name = models.CharField(max_length=210)
    logo = models.ImageField(upload_to='club/')
    league = models.ForeignKey(League, on_delete=models.SET_NULL)


class Statics(models.Model):
    club = models.ForeignKey(Club, on_delete=models.SET_NULL)
    game = models.IntegerField()
    win = models.IntegerField()
    draw = models.IntegerField()
    lose = models.IntegerField()
    score = models.IntegerField()
    conceded = models.IntegerField()
    point = models.IntegerField()
