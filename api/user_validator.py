from leaderboard_app.models import *
from django.core.exceptions import ObjectDoesNotExist


def validate_uuid(user_id):
    try:
        uuid.UUID(user_id)
    except ValueError:
        return False
    return True


def validate_user(user_id):
    if not validate_uuid(user_id):
        return None, "Provide a valid UUID", 400
    try:
        user = Player.objects.get(user_id=user_id)
    except ObjectDoesNotExist:
        return None, "User Does not Exists", 404
    return user, "success", 200
