from leaderboard_app.models import Player
from itertools import islice
from faker import Faker
import random
from leaderboard.leaderboard import Leaderboard
import json

highscore_leaderboard = Leaderboard("highscore")

fake = Faker()
country_codes = ['TR',
                 'US',
                 'FR',
                 'ES',
                 'IT']


def bulk_create(size):
    batch_size = 200
    objs = (Player(display_name=fake.name(), country_iso_code=random.choice(country_codes),
                   points=i) for i in range(int(size)))

    while True:
        batch = list(islice(objs, batch_size))
        if not batch:
            break
        Player.objects.bulk_create(batch, batch_size)


def iterative_create(size):
    for i in range(int(size)):
        Player.objects.create(display_name=fake.name(), country_iso_code=random.choice(country_codes),
                              points=i)


def create_users(size, backend):
    if backend == "django":
        bulk_create(size)
    else:
        iterative_create(size)


def fix_offset_limit(offset, limit):
    offset = int(offset)
    limit = int(limit)
    if offset == 0:
        offset = 1
    starting_rank = int((int(offset) - 2) / int(offset))
    ending_rank = offset + limit

    return starting_rank, ending_rank


def append_extra_data_queryset(queryset, names):
    error = None
    try:
        for s in queryset:
            byte_format = highscore_leaderboard.member_data_for(s["member"])
            json_to_str = byte_format.decode('utf8').replace("'", '"')
            valid_json = json.loads(json_to_str)
            s["member"] = s["member"].decode('utf8')

            for name in names:
                s[name] = valid_json[name]
                s[name] = valid_json[name]
    except Exception as e:
        error = e
        return queryset, error

    return queryset, error


def append_extra_data_user(user, names):
    error = None
    try:
        byte_format = highscore_leaderboard.member_data_for(user["member"])
        json_to_str = byte_format.decode('utf8').replace("'", '"')
        valid_json = json.loads(json_to_str)
        for name in names:
            user[name] = valid_json[name]
            user[name] = valid_json[name]
    except Exception as e:
        error = e
        return user, error

    return user, error


def filter_json(queryset, field, q):
    error = None
    try:
        queryset = [member for member in queryset if member[field] == q]
    except Exception as e:
        error = e
        return queryset, error

    return queryset, error
