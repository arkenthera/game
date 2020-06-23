from leaderboard_app.serializers import *
from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from api.user_validator import validate_user
from leaderboard.leaderboard import Leaderboard
from api.utils import rank_player_objects

highscore_leaderboard = Leaderboard('highscores')


class ScoreSubmitAPIView(CreateAPIView):
    serializer_class = ScoreSubmitSerializer

    def perform_create(self, serializer):
        user_id = self.request.data["user_id"]
        score_worth = self.request.data["score_worth"]
        result = validate_user(user_id)
        user, message = result[0], result[1]
        if user:
            user.points += float(score_worth)
            user.save()
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
        queryset = Player.objects.all()
        page = self.request.query_params.get('page', None)

        country_iso_code = self.kwargs['country_iso_code']
        if country_iso_code:
            queryset = Player.objects.filter(country_iso_code=country_iso_code.upper())
        queryset = rank_player_objects(queryset, page)
        return queryset


class LeaderBoardRedisAPIView(ListAPIView):
    serializer_class = UserLeaderBoardRedisSerializer

    def get_queryset(self):
        queryset = highscore_leaderboard.all_leaders()
        return queryset
