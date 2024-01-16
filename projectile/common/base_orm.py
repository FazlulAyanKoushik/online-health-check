import logging

from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase

from accountio.models import Organization, OrganizationUser
from accountio.choices import OrganizationUserRole, OrganizationUserStatus

from core.models import User
from core.choices import UserType

from doctorio.models import Department

logger = logging.getLogger(__name__)
logger.warning("We are calling orm calls here but we do not like it")


class BaseOrmCallApi(APITestCase):
    # create user
    def get_user(self) -> User:
        logger.warning("Created USER with ORM calls")

        user = get_user_model().objects.create_user("+8801111111111", "test123pass")

        return user

    # create organization
    def create_organization(self) -> Organization:
        logger.warning("Created ORGANIZATION with ORM calls")

        organization = Organization.objects.create(
            name="CardiCheck",
            registration_no="456",
            status=OrganizationUserStatus.ACTIVE,
        )

        return organization

    # create organization user
    def create_organization_user(
        self, organzation: Organization, user: User
    ) -> OrganizationUser:
        logger.warning("Created ORGANIZATION USER with ORM calls")

        organization_user = OrganizationUser.objects.create(
            organization=organzation,
            user=user,
            role=OrganizationUserRole.OWNER,
            status=OrganizationUserStatus.ACTIVE,
            is_default=True,
        )

        return organization_user

    # create department
    def get_department(self):
        logger.warning("Created DEPARTMENT with ORM calls")

        department = Department.objects.create(name="Cardiology")
        return department
