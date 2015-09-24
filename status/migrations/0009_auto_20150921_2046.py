# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0008_auto_20150805_1221'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysis',
            name='age',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='analysis',
            name='age_error',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='analysis',
            name='identifier',
            field=models.IntegerField(default=0),
        ),
    ]
