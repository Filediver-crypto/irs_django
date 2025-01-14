# Generated by Django 5.1.3 on 2025-01-14 12:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookingsystem', '0007_room_building_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bookingsystem.course'),
        ),
    ]
