# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('importer', '0002_auto_20150807_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='importrequest',
            name='is_irradiation',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='importrequest',
            name='imported_date',
            field=models.DateTimeField(default=None),
        ),
    ]
