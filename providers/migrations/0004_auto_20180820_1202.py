# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-08-20 12:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0003_serviceareas'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='serviceareas',
            table='serviceAreas',
        ),
    ]