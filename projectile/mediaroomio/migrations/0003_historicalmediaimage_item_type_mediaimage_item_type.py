# Generated by Django 4.2.1 on 2023-06-09 07:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mediaroomio", "0002_alter_historicalmediaimage_image_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalmediaimage",
            name="item_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("PRESCRIPTION", "Prescription"),
                    ("TEST_REPORT", "Test Report"),
                    ("OTHER", "Other"),
                ],
                default="OTHER",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="mediaimage",
            name="item_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("PRESCRIPTION", "Prescription"),
                    ("TEST_REPORT", "Test Report"),
                    ("OTHER", "Other"),
                ],
                default="OTHER",
                max_length=20,
            ),
        ),
    ]
