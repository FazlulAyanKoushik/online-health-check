from django.contrib.auth import get_user_model
from rest_framework import generics

from core.rest.serializers.users import PrivateMeSerializer

User = get_user_model()


class PrivateMeDetail(generics.RetrieveUpdateAPIView):
    serializer_class = PrivateMeSerializer

    def get_object(self):
        return User.objects.get(id=self.request.user.id)
