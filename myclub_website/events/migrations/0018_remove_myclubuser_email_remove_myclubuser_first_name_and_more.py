# Generated by Django 5.0.1 on 2024-05-17 08:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0017_alter_venue_email_address_alter_venue_web_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myclubuser',
            name='email',
        ),
        migrations.RemoveField(
            model_name='myclubuser',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='myclubuser',
            name='last_name',
        ),
        migrations.AddField(
            model_name='myclubuser',
            name='event',
            field=models.ForeignKey(default=42, on_delete=django.db.models.deletion.CASCADE, to='events.event'),
        ),
        migrations.AddField(
            model_name='myclubuser',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='EventRegistration',
        ),
    ]
