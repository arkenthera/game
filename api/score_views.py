from leaderboard_app.serializers import *
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from api.user_validator import validate_user
from django.db.models import F
from django.db.models.expressions import Window
from django.db.models.functions import DenseRank
from leaderboard.leaderboard import Leaderboard
import json

highscore_leaderboard = Leaderboard("highscore")


class ScoreSubmitAPIView(CreateAPIView):
    serializer_class = ScoreSubmitSerializer

    def perform_create(self, serializer):
        user_id = self.request.data["user_id"]
        score_worth = self.request.data["score_worth"]
        result = validate_user(user_id)
        user, message = result[0], result[1]
        if user:
            point = serializer.save(user=user, score_worth=score_worth)
            return point, "success"
        return None, message

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance, message = self.perform_create(serializer)
        if instance:
            instance_serializer = ScoreSubmitSerializer(instance)
            return Response(instance_serializer.data)
        return Response({"message": message})


class LeaderBoardAPIView(ListAPIView):
    serializer_class = UserLeaderBoardSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        queryset = Player.objects.annotate(rank=Window(
            expression=DenseRank(),
            order_by=F('points').desc(),

        ))

        country_iso_code = self.kwargs['country_iso_code']
        if country_iso_code:
            queryset.filter(country_iso_code=country_iso_code.upper())

        return queryset


class LeaderBoardRedisAPIView(ListAPIView):
    serializer_class = UserLeaderBoardRedisSerializer

    def get_queryset(self):
        limit = int(self.request.query_params.get('limit', 1000))
        offset = int(self.request.query_params.get('offset', 1))

        if offset == 0:
            offset = 1
        # problem in starting index
        starting_rank = int((int(offset) - 2) / int(offset))
        ending_rank = offset + limit

        queryset = highscore_leaderboard.members_from_rank_range(starting_rank=starting_rank, ending_rank=ending_rank)
        for s in queryset:
            byte_format = highscore_leaderboard.member_data_for(s["member"])
            json_to_str = byte_format.decode('utf8').replace("'", '"')
            valid_json = json.loads(json_to_str)
            s["display_name"] = valid_json["display_name"]
            s["country"] = valid_json["country"]

        print(queryset)
        return queryset
