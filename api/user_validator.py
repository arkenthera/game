from leaderboard_app.models import *
from django.core.exceptions import ObjectDoesNotExist

from leaderboard.leaderboard import Leaderboard

highscore_leaderboard = Leaderboard("highscore")


def validate_uuid(user_id):
    try:
        uuid.UUID(user_id)
    except ValueError:
        return False
    return True


def validate_user(user_id):
    if not validate_uuid(user_id):
        return None, None, "Provide a valid UUID", 400

    if highscore_leaderboard.check_member(user_id):
        user = Player.objects.filter(user_id=user_id).first()
        return user, user_id, "success", 200
    return None, None, "User Does not Exists", 404
