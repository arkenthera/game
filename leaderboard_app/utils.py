from leaderboard_app.models import Player
from leaderboard.leaderboard import Leaderboard

highscore_leaderboard = Leaderboard("highscore")


def update_user_data(user):
    highscore_leaderboard.update_member_data(user.user_id,
                                             {"country": user.country_iso_code,
                                              "display_name": user.display_name})
