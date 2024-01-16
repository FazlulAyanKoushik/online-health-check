from rest_framework import status

from common.base_test import BaseApiTestCase

from patientio.rest.tests import payloads, urlhelpers


class PrivatePatientDetails(BaseApiTestCase):
    def test_create_patient(self):
        response = self.patient_create
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_patient(self):
        uid = self.patient_uid
        url = urlhelpers.patient_detail_url(uid)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_patient(self):
        uid = self.patient_uid

        url = urlhelpers.patient_detail_url(uid)

        payload = {
            "name": "John Doe",
            "age": 30,
        }

        response = self.client.put(url, data=payload)

        self.assertEqual(response.status_code, 200)
