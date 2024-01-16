from django.urls import path

from ..views.onboarding import GlobalUserActivation

urlpatterns = [
    path("/activate", GlobalUserActivation.as_view(), name="user-activation"),
]
