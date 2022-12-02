from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    status = models.IntegerField(choices=((1, 'user'), (2, 'admin')), default=1)
    number = models.IntegerField(null=True, blank=True)


class Info(models.Model):     # done
    logo = models.ImageField(upload_to='info/')
    bio = models.TextField()
    phone = models.IntegerField()
    email = models.CharField(max_length=215)
    insta = models.URLField()
    tg = models.URLField()
    fb = models.URLField()
    yt = models.URLField()
    tw = models.URLField()


class Ads(models.Model):  # done
    logo = models.ImageField(upload_to='ads/')
    url = models.URLField()


class Slider(models.Model):  # done
    img = models.ImageField(upload_to='slider/')
    title = models.CharField(max_length=210)
    text = models.TextField(null=True, blank=True)


class Report(models.Model):  # done
    img = models.ImageField(upload_to='report/', null=True, blank=True)
    video = models.FileField(upload_to='report/', null=True, blank=True)
    is_video = models.BooleanField(default=False)
    is_top = models.BooleanField(default=False)
    is_news = models.BooleanField(default=False)
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


class League(models.Model):  # done
    name = models.CharField(max_length=210)
    logo = models.ImageField(upload_to='league/')


class Club(models.Model):  # done
    name = models.CharField(max_length=210)
    logo = models.ImageField(upload_to='club/')
    league = models.ForeignKey(League, on_delete=models.SET_NULL, null=True, blank=True)


class Statics(models.Model):  # done
    club = models.ForeignKey(Club, on_delete=models.SET_NULL, null=True, blank=True)
    game = models.IntegerField(default=0)
    win = models.IntegerField(default=0)
    draw = models.IntegerField(default=0)
    lose = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    conceded = models.IntegerField(default=0)
    point = models.IntegerField(default=0)


class Table(models.Model):  # done
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    year = models.PositiveIntegerField()
    statics = models.ManyToManyField(Statics)


class Player(models.Model):  # done
    club = models.ForeignKey(Club, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=210)
    l_name = models.CharField(max_length=210)
    number = models.IntegerField(null=True, blank=True)
    position = models.IntegerField(choices=(
        (1, 'GK'),
        (2, 'RB'), (3, 'CB'), (4, 'LB'),
        (5, 'CMD'), (6, 'MD'),
        (7, 'RW'), (8, 'LW'), (9, 'ST'),
        (10, 'trainer'), (11, 'sub-trainer'), (12, 'analytic')
    ))
    is_staff = models.BooleanField(default=False)
    birth = models.DateField()
    img = models.ImageField(upload_to='players/')
    sub_on = models.IntegerField(default=0)
    sub_off = models.IntegerField(default=0)
    goals = models.IntegerField(default=0)
    minute = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.position == 10:
            is_staff = True
            self.number = None
        elif self.position == 11:
            is_staff = True
            self.number = None
        elif self.position == 12:
            is_staff = True
            self.number = None
        elif self.number:
            is_staff = False
        elif self.number is None:
            if self.position == 10:
                is_staff = True
                self.number = None
            elif self.position == 11:
                is_staff = True
                self.number = None
            elif self.position == 12:
                is_staff = True
                self.number = None
            else:
                is_staff = False
                self.number = 1
        else:
            is_staff = False
            self.number = 1
        self.is_staff = is_staff
        super(Player, self).save(*args, **kwargs)


class Game(models.Model):  # done
    date = models.DateTimeField()
    status = models.IntegerField(choices=((1, 'not-started'), (2, 'playing'), (3, 'played')))
    guest = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='guest')
    host = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='host')
    guest_goal = models.IntegerField(default=0)
    host_goal = models.IntegerField(default=0)
    mvp = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True)


class Line(models.Model):  # done
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    team = models.ManyToManyField(Player)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)


class Passes(models.Model):  # done
    name = models.CharField(max_length=210)
    all = models.IntegerField()
    successful = models.IntegerField()
    percent = models.IntegerField(null=True, blank=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        success = int(self.successful)
        p = int(self.all)
        percent = success / p * 100
        self.percent = percent
        super(Passes, self).save(*args, **kwargs)


class Substitute(models.Model):  # +
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    squad = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_out')
    line = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_on')
    minute = models.IntegerField()


class Goal(models.Model):  # +
    minute = models.IntegerField()
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, blank=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, blank=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True)


class Detail(models.Model):  # done
    detail = models.CharField(max_length=210, null=True, blank=True)
    img = models.ImageField(upload_to='product/', null=True, blank=True)
    is_img = models.BooleanField(default=False)
    is_order = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.img:
            is_img = True
        else:
            is_img = False
        self.is_img = is_img
        super(Detail, self).save(*args, **kwargs)


class Product(models.Model):  # done
    name = models.CharField(max_length=210)
    bio = models.TextField()
    price = models.FloatField()
    bonus = models.FloatField(default=0)
    info = models.ManyToManyField(Detail, related_name='info')
    image = models.ManyToManyField(Detail, related_name='image')
    available = models.BooleanField()
    rating = models.IntegerField(choices=(
        (1, '1-star'),
        (2, '2-star'),
        (3, '3-star'),
        (4, '4-star'),
        (5, '5-star'),
    ), default=1)


class Wishlist(models.Model):  # -
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class OrderItem(models.Model):  # -
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class Order(models.Model):  # -
    order_item = models.ManyToManyField(OrderItem)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=210)
    l_name = models.CharField(max_length=210)
    number = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    postal = models.CharField(max_length=255)
    email = models.EmailField()
    region = models.ForeignKey(Detail, on_delete=models.CASCADE)
    city = models.CharField(max_length=210)
    status = models.IntegerField(choices=(
        (0, 'accepted'),
        (1, 'preparing'),
        (2, 'finished'),
    ), default=0)


class Chat(models.Model):  # done
    chat = models.CharField(max_length=1000)


class Telegram(models.Model):  # done
    bot_token = models.CharField(max_length=1000)
    chat = models.ManyToManyField(Chat)
