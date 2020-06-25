from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
import uuid


class TimeStamped(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(null=True, editable=False)
    updated = models.DateTimeField(null=True, editable=False)

    def save(self, *args, **kwargs):
        _now = now()
        self.updated = _now
        if not self.id:
            self.created = _now
        super(TimeStamped, self).save(*args, **kwargs)


class LeaderBoard(TimeStamped):
    leaderboard_name = models.CharField(max_length=55, default="highscore")


class CountryCode(models.TextChoices):
    TURKEY = 'TR', _('Turkey')
    USA = 'US', _('United States')
    FRANCE = 'FR', _('France')
    SPAIN = 'ES', _('Spain')
    ITALY = 'IT', _('Italy')


class Player(TimeStamped):
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    leaderboard = models.ForeignKey(LeaderBoard, null=True, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=55)
    country_iso_code = models.CharField(
        max_length=2,
        choices=CountryCode.choices
    )
    points = models.FloatField(default=0.0)
    rank = models.IntegerField(null=True)

    class Meta:
        ordering = ["-points"]


class PointSubmission(TimeStamped):
    user = models.ForeignKey(Player, null=True, on_delete=models.CASCADE)
    score_worth = models.FloatField(default=0.0)
