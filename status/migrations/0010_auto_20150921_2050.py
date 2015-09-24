# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0009_auto_20150921_2046'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='analysis',
            name='runid',
        ),
        migrations.AddField(
            model_name='analysis',
            name='aliquot',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='analysis',
            name='increment',
            field=models.IntegerField(default=0),
        ),
    ]
