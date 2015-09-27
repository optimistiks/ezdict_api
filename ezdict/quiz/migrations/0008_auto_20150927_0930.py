# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0007_auto_20150925_0607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizanswer',
            name='text',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
