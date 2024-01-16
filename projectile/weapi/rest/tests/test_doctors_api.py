from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from common.base_orm import BaseOrmCallApi

from . import payloads, urlhelpers


class PrivateDoctorApiTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # create super user
        self.user = BaseOrmCallApi.super_user()

        # create organization
        self.organization = BaseOrmCallApi.create_organization()

        # connect user and organization
        self.clinic_user = BaseOrmCallApi.create_organization_user(
            self.organization, self.user
        )

        # login user
        self.user_login = self.client.post(
            urlhelpers.user_token_login_url(), payloads.super_user_login_payload()
        )
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.user_login.data["access"]
        )

        # create new user for doctor
        self.new_user = BaseOrmCallApi.get_user()

        # create doctor
        self.post_response = self.client.post(
            urlhelpers.doctor_list_url(), payloads.doctor_payload(self.new_user)
        )
        self.assertEqual(self.post_response.status_code, status.HTTP_201_CREATED)

    def test_create_doctor(self):
        """Test for creating doctor"""

        response = self.post_response

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["name"],
            payloads.doctor_payload(self.new_user)["name"],
        )

    def test_get_doctor(self):
        """Test for getting doctor list"""

        response = self.client.get(urlhelpers.doctor_list_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_retrieve_doctor(self):
        """Test for retrieving doctor detail"""

        response = self.client.get(
            urlhelpers.doctor_detail_url(self.post_response.data["uid"])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["uid"], self.post_response.data["uid"])

    def test_update_doctor(self):
        """Test for updating doctor"""

        payload = {"experience": 4}

        response = self.client.patch(
            urlhelpers.doctor_detail_url(self.post_response.data["uid"]), payload
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["experience"], payload["experience"])

    def test_delete_doctor(self):
        """Test for deleting doctor"""

        response = self.client.delete(
            urlhelpers.doctor_detail_url(self.post_response.data["uid"])
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PrivateDoctorAppointmentApiTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # create super user
        self.super_user = BaseOrmCallApi.super_user()

        # create organization
        self.organization = BaseOrmCallApi.create_organization()

        # create organization user
        self.organization_user = BaseOrmCallApi.create_organization_user(
            self.organization, self.super_user
        )

        # create user for doctor
        self.user_doctor = BaseOrmCallApi.get_new_user()

        # create doctor
        self.doctor = BaseOrmCallApi.create_doctor(self.user_doctor, self.organization)

        # create another user for patient
        self.user_patient = BaseOrmCallApi.get_user()

        # create patient
        self.patient = BaseOrmCallApi.create_patient(self.user_patient)

        # create appointment
        self.appointment = BaseOrmCallApi.create_appointment(
            self.patient, self.doctor, self.organization
        )

        # login organization staff for getting appointment list
        self.user_login = self.client.post(
            urlhelpers.user_token_login_url(), payloads.super_user_login_payload()
        )
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.user_login.data["access"]
        )

    def test_get_appointment(self):
        """Test for doctor get appointment list"""

        response = self.client.get(
            urlhelpers.doctor_appointment_list_url(self.doctor.uid)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_retrieve_appointment(self):
        """Test for doctor retrieve appointment details"""

        response = self.client.get(
            urlhelpers.doctor_appointment_detail_url(
                self.doctor.uid, self.appointment.uid
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["uid"], str(self.appointment.uid))
