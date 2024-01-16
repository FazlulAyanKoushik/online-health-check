from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from common.base_orm import BaseOrmCallApi

from weapi.rest.tests import urlhelpers as we_urlhelpers, payloads as we_payloads

from . import payloads, urlhelpers


class PrivateMeApiTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = BaseOrmCallApi.get_user()

        # login user
        self.user_login = self.client.post(
            we_urlhelpers.user_token_login_url(), we_payloads.user_login_payload()
        )

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.user_login.data["access"]
        )

        # Update me
        self.me_update_response = self.client.patch(
            urlhelpers.me_detail_url(), payloads.me_payload()
        )

        self.assertEqual(self.me_update_response.status_code, status.HTTP_200_OK)

    def test_retrieve_me(self):
        # Test for retrieve user

        response = self.client.get(urlhelpers.me_detail_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["gender"], payloads.me_payload()["gender"])

    def test_update_me(self):
        # Test for update user

        payload = {"blood_group": "A+"}
        response = self.client.patch(urlhelpers.me_detail_url(), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["blood_group"], payload["blood_group"])
