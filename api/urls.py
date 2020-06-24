from api.swagger_views import *
from api.user_views import *
from api.score_views import *
from django.urls import path
from django.conf.urls import url

app_name = 'api'

urlpatterns = [
    # user
    path('user/create', UserCreateAPIView.as_view(), name="create-user"),
    path('user/profile/<user_id>', UserGetAPIView.as_view(), name="get-user"),

    path('user/bulk-create', UserBulkCreateAPIView.as_view(), name="create-user-bulk"),

    # point - score
    path('score/submit', ScoreSubmitAPIView.as_view(), name="score-submit"),

    # leaderboard_app
    # path('leaderboard', LeaderBoardAPIView.as_view(), {"country_iso_code": ""}, name="leaderboard"),
    # path('leaderboard/<country_iso_code>', LeaderBoardAPIView.as_view(), name="leaderboard"),

    path('leaderboard', LeaderBoardRedisAPIView.as_view(), {"country_iso_code": ""}, name="leaderboard-redis"),
    path('leaderboard/<country_iso_code>', LeaderBoardRedisAPIView.as_view(), name="leaderboard-redis"),

    # swagger
    url(r'', schema_view, name="index")

]
