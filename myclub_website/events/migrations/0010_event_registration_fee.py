# Generated by Django 5.0.1 on 2024-04-15 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_remove_event_registration_fee'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='registration_fee',
            field=models.IntegerField(default=0, verbose_name='Registration Fee'),
        ),
    ]
