from rest_framework import status

from common.base_test import OrganizationBaseApiTestCase

from core.rest.tests import payloads as core_payloads

from . import urlhelpers, payloads


class PrivateWePatientsApiTests(OrganizationBaseApiTestCase):
    """Test case for PATIENT API"""

    def setUp(self):
        super(PrivateWePatientsApiTests, self).setUp()

    def test_create_patient(self):
        """Test for create patient by organization"""
        response = self.patient_create
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["first_name"],
            core_payloads.user_patient_payload(self.organization)["first_name"],
        )

    def test_get_patient_list(self):
        """Test for get patient list by organization"""
        response = self.patient_list

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["count"],
            1,
        )

    def test_retrieve_patient(self):
        """Test for retrieve patient details by organization"""

        response = self.client.get(urlhelpers.we_patient_detail_url(self.patient_uid))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data["first_name"],
            core_payloads.user_patient_payload(self.organization)["first_name"],
        )

    def test_update_patient(self):
        """Test for update patient details by organization"""

        payload = {"first_name": "Romeo Rajkumer"}
        response = self.client.patch(
            urlhelpers.we_patient_detail_url(self.patient_uid), payload
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data["first_name"],
            payload["first_name"],
        )


class PrivateWePatientsAppointmentsApiTests(OrganizationBaseApiTestCase):
    """Test case for PATIENT APPOINTMENTS API"""

    def setUp(self):
        super(PrivateWePatientsAppointmentsApiTests, self).setUp()

    def test_get_patient_appointment(self):
        """Test for get patient appointment list by organization"""
        response = self.client.get(
            urlhelpers.we_patient_appointment_list_url(self.patient_uid)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_get_patient_upcoming_appointment(self):
        """Test for get patient upcoming appointment list by organization"""

        response = self.client.get(
            urlhelpers.we_patient_upcoming_appointment_list_url(self.patient_uid)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_get_patient_completed_appointment(self):
        """Test for get patient completed appointment list by organization"""
        create_completed_appointment = self.client.post(
            urlhelpers.we_appointment_list_url(),
            payloads.completed_appointment_payload(),
        )
        response = self.client.get(
            urlhelpers.we_patient_completed_appointment_list_url(self.patient_uid)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
