from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from core.rest.tests import payloads as core_payloads, urlhelpers as core_urlhelpers

from weapi.rest.tests import payloads as we_payloads, urlhelpers as we_urlhelpers

from .base_orm import BaseOrmCallApi


class OrganizationBaseApiTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.base_orm = BaseOrmCallApi()
        self.user = self.base_orm.get_user()

        # create organization
        self.organization = self.base_orm.create_organization()

        # connect user to organization
        self.organization_user = self.base_orm.create_organization_user(
            self.organization, self.user
        )

        # creating a new patient
        self.patient_create = self.client.post(
            core_urlhelpers.user_patient_url(),
            core_payloads.user_patient_payload(self.organization),
        )

        self.assertEqual(self.patient_create.status_code, status.HTTP_201_CREATED)

        # login organization user
        self.user_login = self.client.post(
            we_urlhelpers.user_token_login_url(), we_payloads.user_login_payload()
        )
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.user_login.data["access"]
        )

        self.department = self.base_orm.get_department()

        # creating a new doctor
        self.doctor_create = self.client.post(
            we_urlhelpers.we_doctor_list_url(),
            we_payloads.doctor_payload(self.department),
        )

        self.assertEqual(self.doctor_create.status_code, status.HTTP_201_CREATED)

        self.patient_list = self.client.get(we_urlhelpers.we_patient_list_url())
        self.patient_uid = self.patient_list.data["results"][0]["uid"]

        # create an appointment
        self.appointment_create = self.client.post(
            we_urlhelpers.we_appointment_list_url(),
            we_payloads.appointment_payload(),
        )


class DoctorBaseApiTestCase(APITestCase):
    pass


class PatientBaseApiTestCase(APITestCase):
    pass
