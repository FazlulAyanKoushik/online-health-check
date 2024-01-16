from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from common.base_orm import BaseOrmCallApi

from . import payloads, urlhelpers
from doctorio.models import Doctor


class PrivatePrescriptionApiTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = BaseOrmCallApi.get_user()

        # create patient
        self.patient = BaseOrmCallApi.create_patient(self.user)

        # create new user for doctor
        self.new_user = BaseOrmCallApi.get_new_user()

        # create super user
        self.super_user = BaseOrmCallApi.super_user()

        # create organization
        self.organization = BaseOrmCallApi.create_organization()

        # connect user and organization
        self.organization_user = BaseOrmCallApi.create_organization_user(
            self.organization, self.super_user
        )

        # create doctor
        self.organization_user_login = self.client.post(
            urlhelpers.user_token_login_url(),
            payloads.super_user_login_payload(),
        )
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.organization_user_login.data["access"]
        )
        self.doctor_create = self.client.post(
            urlhelpers.doctor_list_url(), payloads.doctor_payload(self.new_user)
        )
        self.doctor = Doctor.objects.get(uid=self.doctor_create.data["uid"])

        # create appointment
        self.appointment = BaseOrmCallApi.create_appointment(
            self.patient, self.doctor, self.organization
        )

        # doctor's login
        self.doctor_login = self.client.post(
            urlhelpers.user_token_login_url(),
            payloads.doctor_login_payload(),
        )

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.doctor_login.data["access"]
        )

        # doctor create prescription
        self.prescription_post_response = self.client.post(
            urlhelpers.prescription_list_url(self.appointment.uid),
            payloads.prescription_payload(self.appointment),
        )

        # prescription uid
        self.prescription_uid = self.prescription_post_response.data["uid"]

        self.assertEqual(
            self.prescription_post_response.status_code, status.HTTP_201_CREATED
        )

    def test_create_prescription(self):
        # Test doctor create prescription

        response = self.prescription_post_response

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["next_visit"],
            payloads.prescription_payload(self.appointment)["next_visit"],
        )

    def test_get_prescription(self):
        # Test for get prescription list

        response = self.client.get(
            urlhelpers.prescription_list_url(self.appointment.uid)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_retrieve_prescription(self):
        # Test for retrieve prescription detail

        response = self.client.get(
            urlhelpers.prescription_detail_url(
                self.appointment.uid, self.prescription_uid
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["uid"], self.prescription_uid)

    def test_delete_prescription(self):
        # Test for delete prescription

        response = self.client.delete(
            urlhelpers.prescription_detail_url(
                self.appointment.uid, self.prescription_uid
            )
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
