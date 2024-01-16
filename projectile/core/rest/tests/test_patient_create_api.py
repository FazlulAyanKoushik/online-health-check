import logging

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from . import payloads, urlhelpers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PrivatePatientApitests(APITestCase):
    """Patient Create Api Endpoint Test"""

    def setUp(self):
        self.client = APIClient()

    def test_patient_post(self):

        # patient CreateApi Endpoint test
        patient_response = self.client.post(
            urlhelpers.user_patient_url(), payloads.user_patient_payload()
        )

        # Assert that the response is correct
        self.assertEqual(patient_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            patient_response.data["first_name"],
            payloads.user_patient_payload()["first_name"],
        )
        logger.info('Create patient globally')
