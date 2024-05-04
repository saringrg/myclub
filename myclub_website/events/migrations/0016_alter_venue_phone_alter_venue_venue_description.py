# Generated by Django 5.0.1 on 2024-05-04 18:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_alter_event_description_alter_event_registration_fee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='phone',
            field=models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message='Phone number must be exactly 10 digits.', regex='^\\d{10}$')], verbose_name='Contact Phone'),
        ),
        migrations.AlterField(
            model_name='venue',
            name='venue_description',
            field=models.TextField(),
        ),
    ]
