# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0005_auto_20150803_0047'),
    ]

    operations = [
        migrations.CreateModel(
            name='Connections',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('appname', models.CharField(max_length=120)),
                ('devname', models.CharField(max_length=120)),
                ('com', models.CharField(max_length=120)),
                ('address', models.CharField(max_length=120)),
                ('status', models.CharField(max_length=120)),
            ],
        ),
    ]
