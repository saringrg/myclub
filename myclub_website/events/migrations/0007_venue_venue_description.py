# Generated by Django 5.0.1 on 2024-03-06 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_alter_event_options_alter_venue_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='venue_description',
            field=models.TextField(blank=True),
        ),
    ]
