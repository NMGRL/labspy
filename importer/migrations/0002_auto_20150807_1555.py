# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('importer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='importrequest',
            name='imported_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 7, 15, 55, 15, 194146)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='importrequest',
            name='request_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 7, 15, 55, 20, 751712), auto_created=True),
            preserve_default=False,
        ),
    ]
