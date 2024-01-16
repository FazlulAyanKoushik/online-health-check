from appointmentio.choices import AppointmentType, AppointmentFor, AppointmentStatus


def user_login_payload():
    payload = {"phone": "+8801111111111", "password": "test123pass"}

    return payload


def doctor_payload(department):
    payload = {
        "first_name": "Dr.",
        "last_name": "Dipu",
        "phone": "+8801999999999",
        "email": "doctor.dipu@example.com",
        "registration_no": "12233",
        "experience": 5,
        "consultation_fee": 100.00,
        "follow_up_fee": 500.00,
        "check_up_fee": 500.00,
        "password": "123456",
        "departments": department.uid,
        "ssn": "376283",
    }

    return payload


def appointment_payload():
    payload = {
        "appointment_type": AppointmentType.CONSULTATION,
        "appointment_for": AppointmentFor.ME,
        "status": AppointmentStatus.REQUESTED,
        "is_visible": True,
        "phone": "+8802222222222",
    }
    return payload


def completed_appointment_payload():
    payload = {
        "appointment_type": AppointmentType.CONSULTATION,
        "appointment_for": AppointmentFor.ME,
        "status": AppointmentStatus.COMPLETED,
        "is_visible": True,
        "phone": "+8802222222222",
    }
    return payload
