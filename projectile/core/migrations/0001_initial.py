# Generated by Django 4.2.1 on 2023-05-16 11:25

import autoslug.fields
import core.utils
import dirtyfields.dirtyfields
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone
import phonenumber_field.modelfields
import uuid
import versatileimagefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('language', models.CharField(default='en', max_length=2)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(db_index=True, max_length=128, region=None, unique=True, verbose_name='Phone Number')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=core.utils.get_user_slug, unique=True)),
                ('social_security_number', models.CharField(blank=True, max_length=20)),
                ('nid', models.CharField(blank=True, max_length=20)),
                ('avatar', versatileimagefield.fields.VersatileImageField(blank=True, upload_to=core.utils.get_user_media_path_prefix, verbose_name='Avatar')),
                ('hero', versatileimagefield.fields.VersatileImageField(blank=True, upload_to=core.utils.get_user_media_path_prefix, verbose_name='Hero')),
                ('status', models.CharField(choices=[('DRAFT', 'Draft'), ('PLACEHOLDER', 'Placeholder'), ('ACTIVE', 'Active'), ('HIDDEN', 'Hidden'), ('PAUSED', 'Paused'), ('REMOVED', 'Removed')], default='ACTIVE', max_length=20)),
                ('type', models.CharField(choices=[('UNKNOWN', 'Unknown'), ('PATIENT', 'Patient'), ('DOCTOR', 'Doctor'), ('STAFF', 'Staff')], max_length=20)),
                ('gender', models.CharField(blank=True, choices=[('FEMALE', 'Female'), ('MALE', 'Male'), ('UNKNOWN', 'Unknown'), ('OTHER', 'Other')], default='UNKNOWN', max_length=20)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('height', models.FloatField(blank=True, null=True)),
                ('weight', models.IntegerField(blank=True, null=True)),
                ('blood_group', models.CharField(choices=[('UNDEFINED', 'Undefined'), ('A+', 'A Positive'), ('A-', 'A Negative'), ('B+', 'B Positive'), ('B-', 'B Negative'), ('AB+', 'Ab Positive'), ('AB-', 'Ab Negative'), ('O+', 'O Positive'), ('O-', 'O Negative')], default='UNDEFINED', max_length=10)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': ('-date_joined',),
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.UniqueConstraint(condition=models.Q(('nid', ''), _negated=True), fields=('nid',), name='unique_user_nonempty_nid', violation_error_message='NID must be unique.'),
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.UniqueConstraint(condition=models.Q(('email', ''), _negated=True), fields=('email',), name='unique_user_nonempty_email', violation_error_message='Email must be unique.'),
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.UniqueConstraint(condition=models.Q(('social_security_number', ''), _negated=True), fields=('social_security_number',), name='unique_user_nonempty_social_security_number', violation_error_message='Social Security Number must be unique.'),
        ),
    ]
