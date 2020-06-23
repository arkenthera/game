from leaderboard_app.models import Player


def rank_player_objects(queryset, page):
    for i, player in enumerate(queryset):
        player.rank = i + 1
    return queryset
