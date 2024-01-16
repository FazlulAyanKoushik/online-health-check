from rest_framework import status

from common.base_test import BaseApiTestCase

from patientio.rest.tests import payloads, urlhelpers


class PrivateAppointmentListTest(BaseApiTestCase):
    def test_create_appointment(self):
        """Test for create appointment by organization"""
        response = self.appointment_create
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["appointment_type"],
            payloads.patient_appointment_payload(
                organization=self.organization.uid,
                date_time_slot=self.date_time_slot_create,
            ).get("appointment_type"),
        )

    def test_get_appointment(self):
        """Test for get appointment list by organization"""
        response = self.appointment
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_retrieve_appointment(self):
        """Test for retrieve appointment detail by organization"""
        response = self.client.get(
            urlhelpers.patient_appointment_detail_url(
                self.appointment_create.data["uid"]
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["uid"], self.appointment_create.data["uid"])
