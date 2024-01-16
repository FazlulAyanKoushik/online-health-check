from django.contrib.auth import get_user_model

from rest_framework import generics, filters

from core.rest.serializers.users import UserSlimSerializer

from doctorio.rest.permissions import IsOrganizationStaff

User = get_user_model()


class PrivateUserByPhoneNumberDetail(generics.ListAPIView):
    serializer_class = UserSlimSerializer
    permission_classes = [IsOrganizationStaff]
    queryset = User.objects.filter()
    filter_backends = [filters.SearchFilter]
    search_fields = ["phone"]

    def get_queryset(self):
        users = self.request.user.get_organization().get_users()
        return self.queryset.filter(id__in=users)
    