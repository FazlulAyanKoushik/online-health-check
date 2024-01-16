from django.urls import include, path

urlpatterns = [
    path("/appointments", include("weapi.rest.urls.appointments")),
    path("/doctors", include("weapi.rest.urls.doctors")),
    path("/organizations", include("weapi.rest.urls.organizations")),
    path("/patients", include("weapi.rest.urls.patients")),
    path("/get-user", include("weapi.rest.urls.users")),
    path("", include("weapi.rest.urls.we")),
]
