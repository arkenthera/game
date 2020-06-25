from leaderboard_app.serializers import *
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from api.user_validator import validate_user
from django.db.models import F
from django.db.models.expressions import Window
from django.db.models.functions import DenseRank
from api.utils import *

highscore_leaderboard = Leaderboard("highscore")


class ScoreSubmitAPIView(CreateAPIView):
    """
   Submits score to the user with the given user id

    ---
    parameters:
    - name: body
      description: JSON objects containing: user_id, score_worth
        - user_id: ID of the user in UUID format
          required: true
          type: string
        - score_worth: Number of points
          required: true
          type: float
    """
    serializer_class = ScoreSubmitSerializer

    def perform_create(self, serializer):
        user_id = self.request.data["user_id"]
        score_worth = self.request.data["score_worth"]
        result = validate_user(user_id)
        user, user_id, message, status = result[0], result[1], result[2], result[3]
        if user_id:
            if user:
                point = serializer.save(user=user, score_worth=score_worth)
            else:
                point = serializer.save(score_worth=score_worth)
            return point, message, status
        return None, message, status

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance, message, status = self.perform_create(serializer)
        if instance:
            instance_serializer = ScoreSubmitSerializer(instance)
            return Response(instance_serializer.data, status=201)
        return Response({"message": message}, status=status)


class LeaderBoardAPIView(ListAPIView):
    """
   Lists the user by their rank

    ---
    parameters:
    - {{country_iso_code}}: 2 words country iso code (TR, IT, FR, US etc)
      definition: Returns all users if not provided
      required: false
      type: string
    """
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
    """
   Lists the user by their rank

    ---
    parameters:
    - {{country_iso_code}}: 2 words country code (TR, IT, FR, US etc)
      definition: Returns all users if not provided
      required: false
      type: string
    """
    serializer_class = UserLeaderBoardRedisSerializer

    def get_queryset(self):
        limit = self.request.query_params.get('limit', 1000)
        offset = self.request.query_params.get('offset', 1)
        starting_rank, ending_rank = fix_offset_limit(limit, offset)
        queryset = highscore_leaderboard.members_from_rank_range(starting_rank=starting_rank, ending_rank=ending_rank)
        queryset, error = append_extra_data_queryset(queryset, ["country", "display_name"])

        if error:
            return Response("Unexpected Error", status=500)

        country_iso_code = self.kwargs['country_iso_code']
        if country_iso_code:
            queryset, error = filter_json(queryset, "country", country_iso_code.upper())
            if error:
                return Response("Unexpected Error in Filter(Valid country codes: TR, US, ES, IT, FR)", status=400)

        return queryset
