# Generated by Django 4.2.1 on 2023-06-05 07:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appointmentio', '0009_refill_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='refill',
            name='datetime',
        ),
    ]
