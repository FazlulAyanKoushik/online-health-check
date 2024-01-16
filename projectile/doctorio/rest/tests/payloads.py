from appointmentio.choices import AppointmentType


def doctor_appointment_payload(doctor):
    payload = {
        "appointment_type": AppointmentType.GENERAL,
        "complication": "Headache",
        "doctor": doctor,
    }

    return payload


def doctor_name_update():
    payload = {
        "name": "Dr Asma Ali",
    }

    return payload


def doctor_password_reset():
    payload = {
        "password": "test123pass",
        "new_password": "asma1234567",
        "confirm_password": "asma1234567",
    }

    return payload
