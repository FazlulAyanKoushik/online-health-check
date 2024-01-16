def user_patient_payload(organization):
    return {
        "first_name": "john",
        "last_name": "doe",
        "email": "john@gmail.com",
        "phone": "+8802222222222",
        "weight": "19",
        "hight": "4.0",
        "gender": "MALE",
        "password": "test123pass",
        "date_of_birth": "2000-02-02",
        "organization_uid": organization.uid,
        "social_security_number": "983-23-5783",
    }
