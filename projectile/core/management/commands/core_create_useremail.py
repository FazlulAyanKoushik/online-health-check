import csv
import os

from django.core.management.base import BaseCommand, CommandError

from core.models import User, UserEmail
from core.choices import UserEmailStatus


class Command(BaseCommand):
    help = ""

    def handle(self, *args, **options):
        users = User.objects.filter(is_active=True).order_by("created_at")
        for user in users:
            emails = user.useremail_set.filter()
            if not emails.exists():
                user = UserEmail.objects.create(
                    user=user,
                    email=user.email,
                    status=UserEmailStatus.ACTIVE,
                    is_primary=True,
                )
                print(user)
