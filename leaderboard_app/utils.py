from leaderboard_app.models import Player
from leaderboard.leaderboard import Leaderboard

highscore_leaderboard = Leaderboard("highscore")


def rank_player_objects(queryset):
    for i, player in enumerate(queryset):
        player.rank = i + 1
    return queryset


def update_user_data(user):
    highscore_leaderboard.update_member_data(user.user_id,
                                             {"country": user.country_iso_code,
                                              "display_name": user.display_name})
