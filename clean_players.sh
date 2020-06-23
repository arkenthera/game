#!/usr/bin/env bash

python manage.py shell
from leaderboard_app.models import *
Player.objects.all().count()