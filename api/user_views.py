from leaderboard_app.serializers import *
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from api.user_validator import validate_user
from itertools import islice
import random
from faker import Faker


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        return user

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        instance_serializer = UserDisplaySerializer(instance)
        return Response(instance_serializer.data, status=201)


class UserGetAPIView(GenericAPIView):
    serializer_class = UserDisplaySerializer

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        result = validate_user(user_id)
        user, message, status = result[0], result[1], result[2]
        if user:
            instance_serializer = UserDisplaySerializer(user)
            return Response(instance_serializer.data, status=status)
        return Response({"message": message}, status=status)


class UserBulkCreateAPIView(CreateAPIView):

    def create(self, request, *args, **kwargs):
        fake = Faker()
        size = request.data["size"]

        country_codes = ['TR',
                         'US',
                         'FR',
                         'ES',
                         'IT']

        batch_size = 200
        objs = (Player(display_name=fake.name(), rank=0, country_iso_code=random.choice(country_codes),
                       points=i) for i in range(int(size)))

        while True:
            batch = list(islice(objs, batch_size))
            if not batch:
                break
            Player.objects.bulk_create(batch, batch_size)
        return Response({"message": "created"}, status=201)
