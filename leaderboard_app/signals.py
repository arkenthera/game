from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from leaderboard_app.models import PointSubmission, Player
from leaderboard.leaderboard import Leaderboard
from leaderboard_app.utils import update_user_data

highscore_leaderboard = Leaderboard("highscore")


@receiver(post_save, sender=PointSubmission)
def points_handler(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        score_worth = instance.score_worth
        user.points += float(score_worth)
        user.save()
        highscore_leaderboard.change_score_for(user.user_id, instance.score_worth)

        update_user_data(user)


@receiver(post_save, sender=Player)
def player_create_handler(sender, instance, created, **kwargs):
    if created:
        highscore_leaderboard.rank_member(instance.user_id, instance.points,
                                          {"country": instance.country_iso_code,
                                           "display_name": instance.display_name})

        update_user_data(instance)
