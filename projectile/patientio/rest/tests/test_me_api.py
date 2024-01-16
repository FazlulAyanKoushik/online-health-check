from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from appointmentio.choices import AppointmentType

from common.base_orm import BaseOrmCallApi

from weapi.rest.tests import payloads as we_payloads, urlhelpers as we_urlhelpers

from . import payloads, urlhelpers


class PrivatePatientAppointmentTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = BaseOrmCallApi.get_user()

        # create patient
        self.patient = BaseOrmCallApi.create_patient(self.user)

        # login user
        self.user_login = self.client.post(
            we_urlhelpers.user_token_login_url(), we_payloads.user_login_payload()
        )

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.user_login.data["access"]
        )

        # patient create appointment
        self.post_patient_appointment = self.client.post(
            urlhelpers.patient_appointment_list_url(),
            payloads.patient_appointment_payload(self.patient),
        )

        self.patient_appointment_uid = self.post_patient_appointment.data["uid"]

        self.assertEqual(
            self.post_patient_appointment.status_code, status.HTTP_201_CREATED
        )

    def test_create_patient_appointment(self):
        # Test for patient creating appointment

        response = self.post_patient_appointment

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["appointment_type"],
            payloads.patient_appointment_payload(self.patient)["appointment_type"],
        )

    def test_get_patient_appointment(self):
        # Test for getting patient appointment list

        response = self.client.get(urlhelpers.patient_appointment_list_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_retrieve_patient_appointment(self):
        # Test for retrive patient appointment detail

        response = self.client.get(
            urlhelpers.patient_appointment_detail_url(self.patient_appointment_uid)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["complication"],
            payloads.patient_appointment_payload(self.patient)["complication"],
        )

    def test_update_patient_appointment(self):
        # Test for update patient appointment

        payload = {"appointment_type": AppointmentType.FOLLOWUP}

        response = self.client.patch(
            urlhelpers.patient_appointment_detail_url(self.patient_appointment_uid),
            payload,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["appointment_type"], payload["appointment_type"])

    def test_delete_patient_appointment(self):
        # Test for soft delete patient appointment

        response = self.client.delete(
            urlhelpers.patient_appointment_detail_url(self.patient_appointment_uid)
        )

        self.assertEqual(response.data["status"], status.HTTP_404_NOT_FOUND)
