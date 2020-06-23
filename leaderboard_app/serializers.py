from leaderboard_app.models import *
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ValidationError


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ("display_name", "country_iso_code", "points", "rank")


class UserDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ("user_id", "display_name", "rank", "country_iso_code", "points")


class UserLeaderBoardSerializer(serializers.ModelSerializer):
    country = serializers.CharField(source='country_iso_code')

    class Meta:
        model = Player
        fields = ("rank", "points", "display_name", "country")


class ScoreSubmitSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source='user.user_id')

    class Meta:
        model = PointSubmission
        fields = ("user_id", "score_worth")


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10000
    page_size_query_param = 'page_size'
    max_page_size = 100000


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class UserLeaderBoardRedisSerializer(serializers.Serializer):
    member = serializers.CharField(max_length=33)
    rank = serializers.IntegerField()
    score = serializers.FloatField()
