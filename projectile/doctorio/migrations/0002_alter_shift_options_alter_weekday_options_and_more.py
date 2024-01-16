# Generated by Django 4.2.1 on 2023-05-19 05:19

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('doctorio', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shift',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterModelOptions(
            name='weekday',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AddField(
            model_name='shift',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shift',
            name='uid',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AddField(
            model_name='shift',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='weekday',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='weekday',
            name='uid',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AddField(
            model_name='weekday',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]