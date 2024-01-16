# Generated by Django 4.2.1 on 2023-05-22 11:38

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('appointmentio', '0005_remove_prescriptioninformation_treatment'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='blood_group',
            field=models.CharField(choices=[('UNDEFINED', 'Undefined'), ('A+', 'A Positive'), ('A-', 'A Negative'), ('B+', 'B Positive'), ('B-', 'B Negative'), ('AB+', 'Ab Positive'), ('AB-', 'Ab Negative'), ('O+', 'O Positive'), ('O-', 'O Negative')], default='UNDEFINED', max_length=10),
        ),
        migrations.AddField(
            model_name='appointment',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='appointment',
            name='first_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='appointment',
            name='gender',
            field=models.CharField(blank=True, choices=[('FEMALE', 'Female'), ('MALE', 'Male'), ('UNKNOWN', 'Unknown'), ('OTHER', 'Other')], default='UNKNOWN', max_length=20),
        ),
        migrations.AddField(
            model_name='appointment',
            name='last_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='appointment',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name='Phone Number'),
        ),
        migrations.AddField(
            model_name='historicalappointment',
            name='blood_group',
            field=models.CharField(choices=[('UNDEFINED', 'Undefined'), ('A+', 'A Positive'), ('A-', 'A Negative'), ('B+', 'B Positive'), ('B-', 'B Negative'), ('AB+', 'Ab Positive'), ('AB-', 'Ab Negative'), ('O+', 'O Positive'), ('O-', 'O Negative')], default='UNDEFINED', max_length=10),
        ),
        migrations.AddField(
            model_name='historicalappointment',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicalappointment',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='historicalappointment',
            name='first_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='historicalappointment',
            name='gender',
            field=models.CharField(blank=True, choices=[('FEMALE', 'Female'), ('MALE', 'Male'), ('UNKNOWN', 'Unknown'), ('OTHER', 'Other')], default='UNKNOWN', max_length=20),
        ),
        migrations.AddField(
            model_name='historicalappointment',
            name='last_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='historicalappointment',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name='Phone Number'),
        ),
    ]
