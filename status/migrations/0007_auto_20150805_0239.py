# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0006_connections'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connections',
            name='status',
            field=models.BooleanField(),
        ),
    ]
