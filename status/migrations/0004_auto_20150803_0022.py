# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0003_auto_20150802_2353'),
    ]

    operations = [
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('runid', models.CharField(max_length=80)),
                ('start_time', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.RenameModel(
            old_name='CurrentExperiment',
            new_name='Experiment',
        ),
        migrations.RemoveField(
            model_name='currentanalysis',
            name='experiment',
        ),
        migrations.DeleteModel(
            name='CurrentAnalysis',
        ),
        migrations.AddField(
            model_name='analysis',
            name='experiment',
            field=models.ForeignKey(to='status.Experiment'),
        ),
    ]
