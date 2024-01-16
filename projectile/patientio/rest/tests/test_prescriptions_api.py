from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from common.base_orm import BaseOrmCallApi

from weapi.rest.tests import payloads, urlhelpers as we_urlhelpers

from . import urlhelpers


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
        self.doctor = BaseOrmCallApi.create_doctor(self.new_user, self.organization)

        # create appointment
        self.appointment = BaseOrmCallApi.create_appointment(
            self.patient, self.doctor, self.organization
        )

        # doctor's login
        self.doctor_login = self.client.post(
            we_urlhelpers.user_token_login_url(), payloads.doctor_login_payload()
        )

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.doctor_login.data["access"]
        )

        # doctor create prescription
        self.prescription_post_response = self.client.post(
            we_urlhelpers.prescription_list_url(self.appointment.uid),
            payloads.prescription_payload(self.appointment),
        )

        # prescription uid
        self.prescription_uid = self.prescription_post_response.data["uid"]

        self.assertEqual(
            self.prescription_post_response.status_code, status.HTTP_201_CREATED
        )

        # patient login
        self.patient_login = self.client.post(
            we_urlhelpers.user_token_login_url(), payloads.user_login_payload()
        )

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.patient_login.data["access"]
        )

    def test_get_prescription(self):
        # Test for get prescription list

        response = self.client.get(urlhelpers.prescription_list_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_retrieve_prescription(self):
        # Test for retrieve prescription detail

        response = self.client.get(
            urlhelpers.prescription_detail_url(self.prescription_uid)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["next_visit"],
            payloads.prescription_payload(self.appointment)["next_visit"],
        )
