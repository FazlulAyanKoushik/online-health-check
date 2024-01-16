import random
from datetime import datetime

from django.core.management.base import BaseCommand
from django.db import transaction

from faker import Faker

from tqdm import tqdm

from accountio.choices import (
    OrganizationKind,
    OrganizationStatus,
    OrganizationUserStatus,
    OrganizationUserRole,
)
from accountio.models import Organization, OrganizationUser

from appointmentio.models import Appointment

from core.models import User

from doctorio.choices import DoctorStatus
from doctorio.models import Doctor, Department, Expertise

from patientio.models import Patient

fake = Faker()


class Command(BaseCommand):
    help = "This will create your dummy all required data"

    def generate_bangladeshi_phone_number(self):
        prefixes = ["+88017", "+88012", "+88019", "+88015"]
        selected_prefix = random.choice(prefixes)

        # Generate the remaining 8 digits randomly
        remaining_digits = "".join(random.choices("0123456789", k=8))

        # Concatenate the prefix and remaining digits to form the phone number
        phone_number = selected_prefix + remaining_digits

        if User.objects.filter(phone=phone_number).exists():
            self.generate_bangladeshi_phone_number()

        return phone_number

    def handle(self, *args, **options):
        with transaction.atomic():
            super_shahen = User.objects.create_superuser(
                username="+8801752495467",
                phone="+8801752495467",
                password="123456",
                first_name="Saifullah",
                last_name="Shahen",
            )
            super_bappi = User.objects.create_superuser(
                username="+8801309192698",
                phone="+8801309192698",
                password="bappi",
                first_name="AB",
                last_name="Bappi",
            )
            shahen_clinic = Organization.objects.create(
                name="Saif clinic",
                phone="+8801752495466",
                kind=OrganizationKind.CLINIC,
                status=OrganizationStatus.ACTIVE,
            )
            bappi_clinic = Organization.objects.create(
                name="Bappi clinic",
                phone="+8801309192698",
                kind=OrganizationKind.CLINIC,
                status=OrganizationStatus.ACTIVE,
            )
            # adding shahen as an owner of shahen clinic
            OrganizationUser.objects.create(
                organization=shahen_clinic,
                user=super_shahen,
                is_default=True,
                status=OrganizationUserStatus.ACTIVE,
                role=OrganizationUserRole.OWNER,
            )
            # adding bappi as a staff to shahen clinic
            OrganizationUser.objects.create(
                organization=shahen_clinic,
                user=super_bappi,
                status=OrganizationUserStatus.ACTIVE,
                role=OrganizationUserRole.STAFF,
            )
            # adding bappi as an owner to bappi clinic
            OrganizationUser.objects.create(
                organization=bappi_clinic,
                user=super_bappi,
                is_default=True,
                status=OrganizationUserStatus.ACTIVE,
                role=OrganizationUserRole.OWNER,
            )
            # adding shahen as an staff to bappi clinic
            OrganizationUser.objects.create(
                organization=bappi_clinic,
                user=super_shahen,
                status=OrganizationUserStatus.ACTIVE,
                role=OrganizationUserRole.STAFF,
            )
            # creating doctors
            doctors = []
            departments = []
            expertises = []
            for i in tqdm(range(40)):
                dep = Department.objects.create(name=fake.name())
                departments.append(dep)

            for i in tqdm(range(40)):
                exp = Expertise.objects.create(name=fake.name())
                expertises.append(exp)

            for i in tqdm(range(40)):
                phone = self.generate_bangladeshi_phone_number()
                first_name = fake.first_name()
                last_name = fake.last_name()
                user = User.objects.create(
                    username=phone,
                    phone=phone,
                    password="123456",
                    first_name=first_name,
                    last_name=last_name,
                )

                doctor = Doctor.objects.create(
                    user=user,
                    name=first_name + " " + last_name,
                    phone=phone,
                    department=random.choice(departments),
                    expertise=random.choice(expertises),
                    experience=random.randint(1, 10),
                    status=DoctorStatus.ACTIVE,
                    organization=random.choice([bappi_clinic, shahen_clinic]),
                )
                doctors.append(doctor)

            # creating patient
            for _ in tqdm(range(20)):
                phone = self.generate_bangladeshi_phone_number()
                first_name = fake.first_name()
                last_name = fake.last_name()
                user = User.objects.create_user(
                    username=phone,
                    phone=phone,
                    password="123456",
                    first_name=first_name,
                    last_name=last_name,
                )
                patient = Patient.objects.create(
                    user=user,
                    organization=random.choice([bappi_clinic, shahen_clinic]),
                )
                appointment_date = datetime.strptime(fake.date(), "%Y-%m-%d")
                datetime_app = datetime(
                    appointment_date.year,
                    appointment_date.month,
                    appointment_date.day,
                    0,
                    0,
                    0,
                )
                Appointment.objects.create(
                    organization=patient.organization,
                    schedule_start=datetime_app,
                    doctor=random.choice(doctors),
                    patient=patient,
                    creator_user=user,
                )
