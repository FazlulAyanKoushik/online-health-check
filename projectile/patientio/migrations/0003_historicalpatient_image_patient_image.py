# Generated by Django 4.2.1 on 2023-06-06 10:48

from django.db import migrations, models
import patientio.utils
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('patientio', '0002_rename_primarydiseases_primarydisease'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalpatient',
            name='image',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='image',
            field=versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to=patientio.utils.get_patient_image_file_path),
        ),
    ]
