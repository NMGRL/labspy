# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurement',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
