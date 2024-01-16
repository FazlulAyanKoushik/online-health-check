from rest_framework import status

from common.base_test import BaseApiTestCase

from . import payloads, urlhelpers


class PrivatePatientAppointmentRefillTests(BaseApiTestCase):
    def setUp(self):
        super(PrivatePatientAppointmentRefillTests, self).setUp()
        self.refill_create = response = self.client.post(
            urlhelpers.patient_appointment_refill_url(
                self.appointment_create.data["uid"]
            ),
            payloads.patient_appointment_refill_payload(),
        )

    def test_patient_refill_create(self):
        response = self.refill_create
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["message"],
            payloads.patient_appointment_refill_payload()["message"],
        )

    def test_get_patient_appointment_refill_list(self):
        response = self.client.get(
            urlhelpers.patient_appointment_refill_url(
                self.appointment_create.data["uid"]
            )
        )
        print
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_retrieve_patient_appointment_refill(self):
        response = self.client.get(
            urlhelpers.patient_appointment_refill_detail_url(
                self.appointment_create.data["uid"], self.refill_create.data["uid"]
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], self.refill_create.data["message"])

    def test_update_patient_appointment_refill(self):
        payload = {"message": "This is the updated refill message."}
        response = self.client.patch(
            urlhelpers.patient_appointment_refill_detail_url(
                self.appointment_create.data["uid"],
                self.refill_create.data["uid"],
            ),
            payload,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], payload["message"])

    def test_delete_patient_appointment_refill(self):
        response = self.client.delete(
            urlhelpers.patient_appointment_refill_detail_url(
                self.appointment_create.data["uid"],
                self.refill_create.data["uid"],
            )
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
