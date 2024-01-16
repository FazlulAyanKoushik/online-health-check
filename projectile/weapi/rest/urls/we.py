from django.urls import path

from weapi.rest.views.we import PrivateWeDetail

urlpatterns = [
    path(
        r"",
        PrivateWeDetail.as_view(),
        name="we.detail",
    ),
]
