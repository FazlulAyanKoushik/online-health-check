from rest_framework import serializers

from appointmentio.models import Appointment


class PrivateAppointmentSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ["uid", "appointment_type", "appointment_for", "complication"]
