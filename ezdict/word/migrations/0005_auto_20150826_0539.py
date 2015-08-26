# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('word', '0004_auto_20150812_1847'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wordislearned',
            name='user',
        ),
        migrations.AlterUniqueTogether(
            name='wordtolearn',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='wordtolearn',
            name='user',
        ),
        migrations.DeleteModel(
            name='WordIsLearned',
        ),
        migrations.DeleteModel(
            name='WordToLearn',
        ),
    ]
