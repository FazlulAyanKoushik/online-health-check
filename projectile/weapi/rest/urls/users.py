from django.urls import path

from ..views.users import PrivateUserByPhoneNumberDetail

urlpatterns = [
    path("", PrivateUserByPhoneNumberDetail.as_view(), name="we.get-user-detail")
]
