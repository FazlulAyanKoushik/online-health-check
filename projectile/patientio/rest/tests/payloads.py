from appointmentio.choices import AppointmentType, TimeSchedule


def patient_appointment_payload(organization, date_time_slot):
    payload = {
        "appointment_type": AppointmentType.CONSULTATION,
        "complication": "Headache",
        "schedule_start": "2023-07-06 08:30:00",
        "organization": organization,
        "appointment_date": "2023-07-06",
        "appointment_time": "08:30:00",
        "date_time_slot": date_time_slot,
        "weight": 22,
        "height": 3.3,
        "age": 12,
    }

    return payload


def patient_appointment_refill_payload():
    payload = {"message": "This is a test refill."}
    return payload
