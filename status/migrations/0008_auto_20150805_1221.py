# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0007_auto_20150805_0239'),
    ]

    operations = [
        migrations.AddField(
            model_name='connections',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='connections',
            name='username',
            field=models.CharField(default='root', max_length=120),
            preserve_default=False,
        ),
    ]
