from leaderboard_app.models import Player
from itertools import islice
from faker import Faker
import random

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


def create_users(backend, size):
    if backend == "django":
        bulk_create(size)
    else:
        iterative_create(size)
