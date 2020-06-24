from leaderboard_app.serializers import *
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from api.user_validator import validate_user
from django.db.models import F
from django.db.models.expressions import Window
from django.db.models.functions import DenseRank
from api.utils import *

highscore_leaderboard = Leaderboard("highscore")


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        return user

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)

        rank = highscore_leaderboard.rank_for(instance.user_id)
        instance.rank = rank
        instance_serializer = UserDisplaySerializer(instance)
        return Response(instance_serializer.data, status=201)


class UserGetAPIView(GenericAPIView):
    serializer_class = UserLeaderBoardRedisSerializer

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        result = validate_user(user_id)
        user, message, status = result[0], result[1], result[2]
        if user:
            user = highscore_leaderboard.score_and_rank_for(str(user.user_id))
            print(user)
            user, error = append_extra_data_user(user, ["country", "display_name"])
            print(user)
            instance_serializer = self.serializer_class(user)
            return Response(instance_serializer.data, status=status)
        return Response({"message": message}, status=status)


class UserBulkCreateAPIView(CreateAPIView):
    serializer_class = UserBulkCreateSerializer

    def create(self, request, *args, **kwargs):
        size = self.request.data.get('size', None)
        backend = self.request.data.get('backend', None)

        create_users(backend, size)
        return Response({"message": "created"}, status=201)
