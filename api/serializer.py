from rest_framework import serializers
from main.models import *


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
        model = News
        fields = "__all__"


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
        model = Staff
        fields = "__all__"


class DetailOne(serializers.ModelSerializer):
    class Meta:
        model = Detail
        fields = "__all__"


class ProductOne(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class UserOne(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
