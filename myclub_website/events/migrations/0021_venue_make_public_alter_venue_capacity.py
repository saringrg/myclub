# Generated by Django 5.0.1 on 2024-05-18 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0020_venue_capacity'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='make_public',
            field=models.BooleanField(default=False, verbose_name='Make Public'),
        ),
        migrations.AlterField(
            model_name='venue',
            name='capacity',
            field=models.IntegerField(verbose_name='Capacity'),
        ),
    ]
