from django.apps import AppConfig


class LeaderboardConfig(AppConfig):
    name = 'leaderboard_app'

    def ready(self):
        import leaderboard_app.signals
