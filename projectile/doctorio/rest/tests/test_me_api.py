from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase

from common.base_orm import BaseOrmCallApi

from weapi.rest.tests import payloads as we_payloads, urlhelpers as we_urlhelpers

from . import urlhelpers, payloads


class PrivateMeApiTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.base_orm = BaseOrmCallApi()
        self.user = self.base_orm.get_user()
        self.organization = self.base_orm.create_organization()
        self.doctor = self.base_orm.create_doctor(self.user, self.organization)
        self.test_user = get_user_model().objects.create_user("+8801815553322")
        self.patient = self.base_orm.create_patient(self.test_user, self.organization)

        # login user
        self.user_login = self.client.post(
            we_urlhelpers.user_token_login_url(), we_payloads.user_login_payload()
        )

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.user_login.data["access"]
        )

        self.post_doctor_appointment = self.base_orm.create_appointment(
            self.patient, self.doctor, self.organization
        )

        self.doctor_appointment_uid = self.post_doctor_appointment.uid

    def test_doctor_detail(self):
        url = urlhelpers.doctor_detail_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["email"], "doctor_1@example.com")

    def test_doctor_update_name(self):
        url = urlhelpers.doctor_update_name_url()
        response = self.client.put(url, payloads.doctor_name_update())
        self.assertEqual(response.status_code, 200)
        url = urlhelpers.doctor_detail_url()
        response = self.client.get(url)
        self.assertEqual(response.data["name"], "Dr Asma Ali")

    def test_doctor_reset_password(self):
        url = urlhelpers.doctor_reset_password_url()
        response = self.client.put(url, payloads.doctor_password_reset())
        self.assertEqual(response.status_code, 200)
