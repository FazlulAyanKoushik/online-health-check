from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from common.base_orm import BaseOrmCallApi

from weapi.rest.tests import payloads as we_payloads, urlhelpers as we_urlhelpers

from . import urlhelpers


class PublicOrganizationsTest(APITestCase):
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

        # login organization user
        self.user_login = self.client.post(
            we_urlhelpers.user_token_login_url(), we_payloads.user_login_payload()
        )
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.user_login.data["access"]
        )
        # creating a new doctor
        self.doctor_create = self.client.post(
            we_urlhelpers.doctor_list_url(), we_payloads.doctor_payload()
        )

        self.assertEqual(self.doctor_create.status_code, status.HTTP_201_CREATED)

    def test_organization_list(self):
        response = self.client.get(urlhelpers.public_organization_list_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"], self.organization.name)

    def test_organization_doctor_list(self):
        response = self.client.get(
            urlhelpers.public_organization_doctor_list_url(self.organization.slug)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["results"][0]["email"], we_payloads.doctor_payload()["email"]
        )
        self.assertEqual(response.data["count"], 1)

    def test_organization_doctor_retrieve(self):
        url = urlhelpers.public_organization_doctor_detail_url(
            self.organization.slug, self.doctor_create.data["slug"]
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], we_payloads.doctor_payload()["email"])
