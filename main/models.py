from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    status = models.IntegerField(choices=((1, 'user'), (2, 'admin')), default=1)
    number = models.IntegerField(null=True, blank=True)


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
    is_video = models.BooleanField(default=False)
    is_top = models.BooleanField(default=False)
    date = models.DateTimeField()
    bio = models.CharField(max_length=210)
    author = models.CharField(max_length=210)

    def save(self, *args, **kwargs):
        if self.video:
            is_video = True
        else:
            is_video = False
        self.is_video = is_video
        super(Report, self).save(*args, **kwargs)


class News(models.Model):
    img = models.ImageField(upload_to='news/', null=True, blank=True)
    text = models.TextField()
    title = models.CharField(max_length=210)


class League(models.Model):
    name = models.CharField(max_length=210)
    logo = models.ImageField(upload_to='league/')


class Club(models.Model):
    name = models.CharField(max_length=210)
    logo = models.ImageField(upload_to='club/')
    league = models.ForeignKey(League, on_delete=models.SET_NULL, null=True, blank=True)


class Statics(models.Model):
    club = models.ForeignKey(Club, on_delete=models.SET_NULL, null=True, blank=True)
    game = models.IntegerField(default=0)
    win = models.IntegerField(default=0)
    draw = models.IntegerField(default=0)
    lose = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    conceded = models.IntegerField(default=0)
    point = models.IntegerField(default=0)


class Table(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    year = models.PositiveIntegerField(max_length=4)
    statics = models.ManyToManyField(Statics)


class Player(models.Model):
    club = models.ForeignKey(Club, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=210)
    l_name = models.CharField(max_length=210)
    number = models.IntegerField()
    position = models.IntegerField(choices=(
        (1, 'GK'),
        (2, 'RB'), (3, 'CB'), (4, 'LB'),
        (5, 'CMD'), (6, 'MD'),
        (7, 'RW'), (8, 'LW'), (9, 'ST')
    ))
    birth = models.DateField()
    img = models.ImageField(upload_to='players/')
    goals = models.IntegerField(default=0)


class Staff(models.Model):
    name = models.CharField(max_length=210)
    l_name = models.CharField(max_length=210)
    birth = models.DateField()
    role = models.IntegerField(choices=(
        (1, 'trainer'),
        (2, 'sub-trainer'),
        (3, 'analytic'),
        (4, 'admin')
    ))
    img = models.ImageField(upload_to='staff/')
    club = models.ForeignKey(Club, on_delete=models.SET_NULL, null=True, blank=True)


class Game(models.Model):
    date = models.DateTimeField()
    is_played = models.BooleanField(default=False)
    guest = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='guest')
    host = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='host')
    guest_goal = models.IntegerField(default=0)
    host_goal = models.IntegerField(default=0)


class Line(models.Model):
    team = models.ManyToManyField(Player)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)


class Passes(models.Model):
    all = models.IntegerField()
    successful = models.IntegerField()
    percent = models.IntegerField(null=True, blank=True)
    status = models.IntegerField(choices=(
        (1, 'passes'),
        (2, 'long-passes'),
        (3, 'helps'),
        (4, 'crosses')
    ))

    def save(self, *args, **kwargs):
        percent = self.successful % self.all * 100
        self.percent = percent
        super(Passes, self).save(*args, **kwargs)


class Substitute(models.Model):
    squad = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_out')
    line = models.ForeignKey(Line, on_delete=models.CASCADE, related_name='player_on')
    minute = models.IntegerField()


class Action(models.Model):
    minute = models.IntegerField()
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    action = models.IntegerField(choices=((1, 'red-card'), (2, 'yellow-card')))
    game = models.ForeignKey(Game, on_delete=models.CASCADE)


class Goal(models.Model):
    minute = models.IntegerField()
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, blank=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, blank=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True)


class Detail(models.Model):
    detail = models.CharField(max_length=210, null=True, blank=True)
    img = models.ImageField(upload_to='product/')
    is_img = models.BooleanField()


class Product(models.Model):
    name = models.CharField(max_length=210)
    bio = models.TextField()
    price = models.FloatField()
    bonus = models.FloatField(default=0)
    info = models.ManyToManyField(Detail)
    available = models.BooleanField()
    rating = models.IntegerField(choices=(
        (1, '1-star'),
        (2, '2-star'),
        (3, '3-star'),
        (4, '4-star'),
        (5, '5-star'),
    ), default=1)


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Region(models.Model):
    name = models.CharField(max_length=210)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class Order(models.Model):
    order_item = models.ManyToManyField(OrderItem)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=210)
    l_name = models.CharField(max_length=210)
    number = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    postal = models.CharField(max_length=255)
    email = models.EmailField()
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    city = models.CharField(max_length=210)
    status = models.IntegerField(choices=(
        (0, 'accepted'),
        (1, 'preparing'),
        (2, 'finished'),
    ), default=0)


class Chat(models.Model):
    chat_id = models.CharField(max_length=1000)


class Telegram(models.Model):
    bot_token = models.CharField(max_length=1000)
    chat_id = models.ManyToManyField(Chat)
