# Generated by Django 4.2.1 on 2023-05-17 05:44

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('accountio', '0002_affiliation_doctor_affiliation_organization_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalorganization',
            name='categories',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='categories',
        ),
        migrations.AlterField(
            model_name='historicalorganization',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(db_index=True, max_length=128, region=None, verbose_name='Phone Number'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(db_index=True, max_length=128, region=None, unique=True, verbose_name='Phone Number'),
        ),
    ]
