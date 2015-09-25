# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0006_quiz_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='type',
            field=models.CharField(max_length=50),
        ),
    ]
