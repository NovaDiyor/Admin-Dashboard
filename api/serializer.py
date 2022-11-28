from rest_framework import serializers
from main.models import *


class UserOne(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'date_joined', 'number', 'status', 'email']


class InfoOne(serializers.ModelSerializer):
    class Meta:
        model = Info
        fields = "__all__"


class AdsOne(serializers.ModelSerializer):
    class Meta:
        model = Ads
        fields = "__all__"


class SliderOne(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = "__all__"


class ReportOne(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = "__all__"


class NewOne(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['img', 'bio', 'author', 'date']


class LeagueOne(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = "__all__"


class ClubOne(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = "__all__"


class PlayerOne(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = "__all__"


class StaffOne(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['club', 'name', 'l_name', 'birth', 'position', 'img']


class GameOne(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = "__all__"


class SubOne(serializers.ModelSerializer):
    class Meta:
        model = Substitute
        fields = "__all__"


class LineOne(serializers.ModelSerializer):
    class Meta:
        model = Line
        fields = "__all__"


class GoalOne(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = "__all__"


class PassOne(serializers.ModelSerializer):
    class Meta:
        model = Passes
        fields = "__all__"


class StaticOne(serializers.ModelSerializer):
    class Meta:
        model = Statics
        fields = "__all__"


class TableOne(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = "__all__"


class DetailOne(serializers.ModelSerializer):
    class Meta:
        model = Detail
        fields = "__all__"


class ProductOne(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class WishlistOne(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = "__all__"


class OrderItemOne(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderOne(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class ChatOne(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = "__all__"


class TelegramOne(serializers.ModelSerializer):
    class Meta:
        model = Telegram
        fields = "__all__"
