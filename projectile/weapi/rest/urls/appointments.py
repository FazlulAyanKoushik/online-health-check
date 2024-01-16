from django.urls import path

from ..views.appointments import (
    PrivateAppointmentDetail,
    PrivateAppointmentList,
    PrivateAppointmentScheduleCreate,
    PrivateAppointmentTimeSlotList,
)

urlpatterns = [
    path(
        "/time-slots",
        PrivateAppointmentTimeSlotList.as_view(),
        name="we.appointment-time-slot-list",
    ),
    path(
        "/schedules",
        PrivateAppointmentScheduleCreate.as_view(),
        name="we.appointment-schedule-create",
    ),
    path(
        "/<uuid:uid>",
        PrivateAppointmentDetail.as_view(),
        name="we.appointment-detail",
    ),
    path(
        "",
        PrivateAppointmentList.as_view(),
        name="we.appointment-list",
    ),
]
