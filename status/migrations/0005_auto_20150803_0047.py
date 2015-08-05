# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0004_auto_20150803_0022'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysis',
            name='analysis_type',
            field=models.CharField(default='unknown', max_length=80),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='experiment',
            name='state',
            field=models.CharField(default='finished', max_length=80),
            preserve_default=False,
        ),
    ]
