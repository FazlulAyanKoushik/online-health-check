from rest_framework import status

from common.base_test import BaseApiTestCase

from weapi.rest.tests import payloads as we_payloads, urlhelpers as we_urlhelpers

from . import urlhelpers


class PrivateDoctorPatientAppointmentTest(BaseApiTestCase):
    def setUp(self):
        super(PrivateDoctorPatientAppointmentTest, self).setUp()
        self.doctor_login_payload = {
            "phone": we_payloads.doctor_payload()["phone"],
            "password": we_payloads.doctor_payload()["password"],
        }
        self.doctor_login = self.client.post(
            we_urlhelpers.user_token_login_url(), self.doctor_login_payload
        )
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.doctor_login.data["access"]
        )

    def test_get_doctor_appointment_patient_list(self):
        response = self.client.get(urlhelpers.doctor_appointment_patient_list_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_doctor_appointment_patient_detail(self):
        response = self.client.get(
            urlhelpers.doctor_appointment_patient_detail_url(
                self.appointment_create.data["uid"]
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["uid"], self.appointment_create.data["uid"])
