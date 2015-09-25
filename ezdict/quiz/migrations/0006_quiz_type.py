# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_auto_20150922_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='type',
            field=models.SlugField(default='to_study'),
            preserve_default=False,
        ),
    ]
