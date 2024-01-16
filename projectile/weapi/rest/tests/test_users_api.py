from rest_framework import status

from common.base_test import OrganizationBaseApiTestCase

from . import urlhelpers


class PrivateUserApiTests(OrganizationBaseApiTestCase):
    """Test case for USER API"""

    def setUp(self):
        super(PrivateUserApiTests, self).setUp()

    def test_user_list(self):
        """Test for user retrieve by phone number"""
        response = self.client.get(urlhelpers.we_user_detail_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
