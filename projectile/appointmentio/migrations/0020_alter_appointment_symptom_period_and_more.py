# Generated by Django 4.2.1 on 2023-07-17 09:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("appointmentio", "0019_alter_appointmentdatetimeslotconnector_appointment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="appointment",
            name="symptom_period",
            field=models.CharField(
                blank=True,
                choices=[
                    ("HOURS", "Hours"),
                    ("DAYS", "Days"),
                    ("WEEKS", "Weeks"),
                    ("MONTHS", "Months"),
                    ("SIX_MONTHS_OR_MORE", "Six months or more"),
                ],
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="historicalappointment",
            name="symptom_period",
            field=models.CharField(
                blank=True,
                choices=[
                    ("HOURS", "Hours"),
                    ("DAYS", "Days"),
                    ("WEEKS", "Weeks"),
                    ("MONTHS", "Months"),
                    ("SIX_MONTHS_OR_MORE", "Six months or more"),
                ],
                max_length=30,
            ),
        ),
        migrations.DeleteModel(
            name="DateTimeSlot",
        ),
    ]
