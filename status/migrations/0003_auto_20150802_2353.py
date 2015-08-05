# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0002_measurement_pub_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrentAnalysis',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('runid', models.CharField(max_length=80)),
                ('start_time', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='CurrentExperiment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('system', models.CharField(max_length=80)),
                ('name', models.CharField(max_length=140)),
                ('user', models.CharField(max_length=80)),
                ('start_time', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.AddField(
            model_name='currentanalysis',
            name='experiment',
            field=models.ForeignKey(to='status.CurrentExperiment'),
        ),
    ]
