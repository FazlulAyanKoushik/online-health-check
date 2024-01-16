# Generated by Django 4.2.1 on 2023-05-17 10:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patientio', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('doctorio', '0001_initial'),
        ('appointmentio', '0002_appointment_doctor_appointment_organization_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='historicalappointment',
            name='phone',
        ),
        migrations.AddField(
            model_name='appointment',
            name='creator_user',
            field=models.ForeignKey(default=1, help_text='Only current logged in user who is creating a appointment, must have to set here.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalappointment',
            name='creator_user',
            field=models.ForeignKey(blank=True, db_constraint=False, help_text='Only current logged in user who is creating a appointment, must have to set here.', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='doctor',
            field=models.ForeignKey(blank=True, help_text='Doctor can be null. Clinic can set the doctor later.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='doctorio.doctor'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(help_text='Who is the patient, is the instance for this field. ', on_delete=django.db.models.deletion.CASCADE, to='patientio.patient'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='schedule_end',
            field=models.DateTimeField(blank=True, help_text='Appointment schedule end time', null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='schedule_start',
            field=models.DateTimeField(blank=True, help_text='Appointment schedule start time', null=True),
        ),
        migrations.AlterField(
            model_name='historicalappointment',
            name='doctor',
            field=models.ForeignKey(blank=True, db_constraint=False, help_text='Doctor can be null. Clinic can set the doctor later.', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='doctorio.doctor'),
        ),
        migrations.AlterField(
            model_name='historicalappointment',
            name='patient',
            field=models.ForeignKey(blank=True, db_constraint=False, help_text='Who is the patient, is the instance for this field. ', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='patientio.patient'),
        ),
        migrations.AlterField(
            model_name='historicalappointment',
            name='schedule_end',
            field=models.DateTimeField(blank=True, help_text='Appointment schedule end time', null=True),
        ),
        migrations.AlterField(
            model_name='historicalappointment',
            name='schedule_start',
            field=models.DateTimeField(blank=True, help_text='Appointment schedule start time', null=True),
        ),
    ]