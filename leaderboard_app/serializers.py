from leaderboard_app.models import *
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ("display_name", "country_iso_code", "points")


class UserDisplaySerializer(serializers.ModelSerializer):
    rank = serializers.IntegerField()

    class Meta:
        model = Player
        fields = ("user_id", "display_name", "rank", "country_iso_code", "points")


class UserLeaderBoardSerializer(serializers.ModelSerializer):
    rank = serializers.IntegerField()
    country = serializers.CharField(source='country_iso_code')

    class Meta:
        model = Player
        fields = ("rank", "points", "display_name", "country", "rank")


class ScoreSubmitSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source='user.user_id')

    class Meta:
        model = PointSubmission
        fields = ("user_id", "score_worth")


class UserBulkCreateSerializer(serializers.Serializer):
    number_of_objects = serializers.IntegerField()


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 5000
    page_size_query_param = 'page_size'
    max_page_size = 100000


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class UserLeaderBoardRedisSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=33, source="member")
    rank = serializers.IntegerField()
    score = serializers.FloatField()
    display_name = serializers.CharField(max_length=33)
    country = serializers.CharField(max_length=2)
